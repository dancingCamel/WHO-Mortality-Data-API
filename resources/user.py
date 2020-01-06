from flask import render_template, make_response, url_for, request, redirect, flash
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh
from auth import requireAdmin, requireApiKey
from base64 import b64encode
from os import urandom
from models.blacklist import BlacklistModel
from models.user import UserModel
import re


class UserRegister(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)

    def post(self):
        # username is just user's email address
        username = request.form.get("username")
        password = request.form.get("password")

        # validate username and password
        def valid_username(username):
            pattern = "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            if re.match(pattern, username):
                return True
            return False

        if not valid_username(username):
            message = "Please enter a valid email address as your username."
            flash(message, 'error')
            return redirect(url_for('userregister'))

        if len(username) > 80:
            message = "Username too long."
            flash(message, 'error')
            return redirect(url_for('userregister'))

        if len(password) == 0:
            message = "Please enter a password."
            flash(message, 'error')
            return redirect(url_for('userregister'))

        # check to see if username already exists
        user = UserModel.find_by_username(username)

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            message = "Email address already exists"
            flash(message, 'error')
            return redirect(url_for('userregister'))

        # hash password
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=32)

        # generate api key and check not already used
        api_key = str(b64encode(urandom(64)).decode('latin1'))[0:64]
        all_blacklist = [
            blacklist.api_key for blacklist in BlacklistModel.find_all()]
        while UserModel.find_by_key(api_key) or api_key in all_blacklist:
            api_key = str(b64encode(urandom(64)).decode('latin1'))[0:64]

        # create new user
        new_user = UserModel(username, hashed_password, api_key)

        # add the new user to the database
        try:
            new_user.save_to_db()
            message = "Registered successfully. Please log in."
            flash(message, 'info')
        except:
            message = "Something went wrong. Please try again later."
            flash(message, 'error')
            return redirect(url_for('userregister'))

        return redirect(url_for('userlogin'))


class User(Resource):
    @classmethod
    @requireAdmin
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        return user.json()

    @classmethod
    @requireAdmin
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        user.delete_from_db()
        return {'message': "User deleted"}


class UserPassword(Resource):
    # don't redirect users as json expected as return
    @login_required
    def put(self):
        # get info
        old_password = request.headers.get('oldPassword')
        old_password2 = request.headers.get('oldPassword2')
        new_password = request.headers.get('password')
        username = request.headers.get('username')

        fresh = login_fresh()
        if not fresh:
            return {'message': "To protect your account, please <a href='/login'>reauthenticate.</a>"}, 401

        # check old pass and new pass match
        if old_password != old_password2:
            error = "Please check your credentials - missmatch."
            return {'message': error}, 401

        # check user exists and password is correct
        user = UserModel.find_by_username(username)

        if not user or not check_password_hash(user.password, old_password):
            error = "Please check your credentials."
            return {'message': error}, 401

        # update password
        hashed_new_password = generate_password_hash(
            new_password, method='pbkdf2:sha256', salt_length=32)

        try:
            user.password = hashed_new_password
            user.save_to_db()
            message = "Successfully updated password."
            return {'message': message}, 201
        except:
            error = "Something went wrong updating your password."
            return {'message': error}, 500


class UserApiKey(Resource):
    # don't redirect users as json expected as return
    @login_required
    def put(self):
        username = request.headers.get('username')
        api_key = request.headers.get('api_key')

        user = UserModel.find_by_username(username)

        fresh = login_fresh()
        if not fresh:
            return {'message': "To protect your account, please <a href='/login'>reauthenticate.</a>."}, 401

        if not user:
            return {'message': "User not found. Try loggin in again."}

        # check current api_key matches one sent by user
        if user.api_key != api_key:
            return {'message': "Something isn't right. Try logging in again."}

        # generate api key and check not already used or in blacklist
        new_api_key = str(b64encode(urandom(64)).decode('latin1'))[0:64]

        all_blacklist = [
            blacklist.api_key for blacklist in BlacklistModel.find_all()]
        while UserModel.find_by_key(new_api_key) or new_api_key in all_blacklist:
            new_api_key = str(b64encode(urandom(64)).decode('latin1'))[0:64]

        # update api key in user database
        try:
            blacklist_entry = BlacklistModel(api_key)
            blacklist_entry.save_to_db()
            user.api_key = new_api_key
            user.save_to_db()
        except:
            return {'message': "Something went wrong generating a new key. Try again later."}

        # return new api_key
        return {'new_api_key': new_api_key}, 201


class UserLogin(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    @classmethod
    def post(cls):
        username = request.form.get('username')
        password = request.form.get('password')
        rememberBool = True if request.form.get('remember') else False

        # find user in db
        user = UserModel.find_by_username(username)

        # check if user actually exists
        if not user or not check_password_hash(user.password, password):
            # if user doesn't exist or password is wrong, reload the page
            message = "Please check your login credentials."
            flash(message, 'error')
            return redirect(url_for('userlogin'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=rememberBool)

        return redirect(url_for('profile'))


class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('index'))
