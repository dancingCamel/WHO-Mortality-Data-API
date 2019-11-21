from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)

from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank.",
                          location="form"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank.",
                          location="form"
                          )


class UserRegister(Resource):
    def get(self):
        # show template here
        pass

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # hash password
        hashed_password = generate_password_hash(
            data['password'], method='pbkdf2:sha256', salt_length=32)
        user = UserModel(data['username'], hashed_password)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': "User not found"}, 404
        user.delete_from_db()
        return {'message': "User deleted"}


class UserLogin(Resource):
    def get(self):
        # show template here
        pass

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        # find user in db
        user = UserModel.find_by_username(data['username'])

        # check password and create tokens if correct
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            # create a refresh token, too
            refresh_token = create_refresh_token(identity=user.id)

            # return the tokens to the client
            return {
                'access_token': access_token,
                # this token never changes
                'refresh_token': refresh_token
            }, 200

        # return error string if user not found or password incorrect
        return {'message': "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': "Successfully logged out."}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    # if we get past the decorator we definitely have a refresh token
    def post(self):
        # get_jwt_identity uses both access and refresh tokens. returns user_id in this case (as the identity we set is the id)
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
