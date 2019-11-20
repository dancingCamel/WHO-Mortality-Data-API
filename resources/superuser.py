from flask_restful import Resource, reqparse
from models.superuser import SuperuserModel

_superuser_parser = reqparse.RequestParser()
_superuser_parser.add_argument('username',
                               type=str,
                               required=True,
                               help="This field cannot be blank."
                               )


class Superuser(Resource):
    @classmethod
    def get(cls, username):
        superuser = SuperuserModel.find_by_username(username)
        if not superuser:
            return {'message': "Superuser not found"}, 404
        return superuser.json()


class SuperuserUpdate(Resource):
    def post(self):
        data = _superuser_parser.parse_args()

        if SuperuserModel.find_by_username(data['username']):
            return {"message": "A superuser with that username already exists"}, 400

        superuser = SuperuserModel(**data)
        superuser.save_to_db()

        return {"message": "Superuser created successfully."}, 201

    def put(self):
        data = _superuser_parser.parse_args()
        pass

    def delete(self):
        data = _superuser_parser.parse_args()
        superuser = SuperuserModel.find_by_username(data['username'])

        if not superuser:
            return {'message': "Superuser not found"}, 404
        superuser.delete_from_db()
        return {'message': "Superuser deleted"}
