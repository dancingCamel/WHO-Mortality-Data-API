from flask_restful import Resource, reqparse
from models.superuser import SuperuserModel
from models.user import UserModel
from auth import requireAdmin

_superuser_parser = reqparse.RequestParser()
_superuser_parser.add_argument('username',
                               type=str,
                               required=True,
                               help="This field cannot be blank."
                               )


class Superuser(Resource):
    @requireAdmin
    def get(self, username):
        superuser = SuperuserModel.find_by_username(username)
        if not superuser:
            return {'message': "Superuser not found"}, 404
        return superuser.json()


class SuperuserUpdate(Resource):
    @requireAdmin
    def post(self):
        data = _superuser_parser.parse_args()

        if SuperuserModel.find_by_username(data['username']):
            return {'message': "A superuser with that username already exists"}, 400

        user = UserModel.find_by_username(data['username'])
        if not user:
            return {'message': "User not found (a superuser must be a user first)."}, 404

        user = user.json()
        superuser = SuperuserModel(
            username=user['username'])

        superuser.save_to_db()

        return {"message": "Superuser created successfully."}, 201

    @requireAdmin
    def delete(self):
        data = _superuser_parser.parse_args()

        superuser = SuperuserModel.find_by_username(data['username'])

        if not superuser:
            return {'message': "Superuser not found"}, 404
        superuser.delete_from_db()
        return {'message': "Superuser deleted"}
