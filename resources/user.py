from flask import render_template, make_response, url_for, request, redirect, flash
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from base64 import b64encode
from os import urandom


from models.user import UserModel
from blacklist import BLACKLIST

# reqparse returns python dictionaries.
_user_parser = reqparse.RequestParser()
# _user_parser.add_argument('username',
#                           type=str,
#                           required=True,
#                           help="This field cannot be blank.",
#                           location="form"
#                           )
# _user_parser.add_argument('password',
#                           type=str,
#                           required=True,
#                           help="This field cannot be blank.",
#                           location="form"
#                           )


class UserRegister(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)

    def post(self):
        # data = _user_parser.parse_args()
        username = request.form.get("username")
        password = request.form.get("password")
        # username = data['username']
        # password = data['password']

        # if this returns a user, then the email already exists in database
        user = UserModel.find_by_username(username)

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('userregister'))

        # hash password
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=32)

        # generate api key and check not already used
        api_key = str(b64encode(urandom(64)).decode('latin1'))
        while UserModel.find_by_key(api_key):
            api_key = str(b64encode(urandom(64)).decode('latin1'))

        # create new user
        new_user = UserModel(username, hashed_password, api_key)

        # add the new user to the database
        try:
            new_user.save_to_db()
            message = "Registered successfully. Please log in."
        except:
            message = "Something went wrong registering the user."
            flash(message)
            return redirect(url_for('userregister', message=message))

        if message:
            flash(message)
        return redirect(url_for('userlogin', message=message))

    # need user put method to change password or api_ley


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        user.delete_from_db()
        return {'message': "User deleted"}


class UserLogin(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    @classmethod
    def post(cls):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # find user in db
        user = UserModel.find_by_username(username)

        # check if user actually exists
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if user doesn't exist or password is wrong, reload the page
            return redirect(url_for('userlogin'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)

        # save api_key to session storage

        return redirect(url_for('profile'))


class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('index'))
