from flask_restful import Resource, reqparse
from models.subdiv import SubdivModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_claims
)


class Subdiv(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required")

    @jwt_required
    def get(self, subdiv_code):
        subdiv = SubdivModel.find_by_code(subdiv_code)
        if subdiv:
            return subdiv.json()
        return {'message': "Subdiv {} not found".format(subdiv_code)}, 404

    @fresh_jwt_required
    def post(self, subdiv_code):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        data = Subdiv.parser.parse_args()
        subdiv = SubdivModel.find_by_code(subdiv_code)

        if subdiv:
            return {'message': "A subdiv already exists with code '{}'".format(subdiv_code)}, 400

        subdiv = SubdivModel(subdiv_code, data['description'])
        try:
            subdiv.save_to_db()
        except:
            return {'message': "There was an error inserting the subdiv."}, 500
        return subdiv.json(), 201

    @fresh_jwt_required
    def put(self, subdiv_code):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        data = Subdiv.parser.parse_args()
        subdiv = SubdivModel.find_by_code(subdiv_code)

        if subdiv:
            subdiv.description = data['description']
        else:
            subdiv = SubdivModel(subdiv_code, data['description'])

        try:
            subdiv.save_to_db()
        except:
            return {'message': "There was an error inserting the subdiv."}, 500

        return subdiv.json(), 201

    @fresh_jwt_required
    def delete(self, subdiv_code):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        subdiv = SubdivModel.find_by_code(subdiv_code)

        if subdiv:
            subdiv.delete_from_db()
            return {'message': "Subdiv '{}' deleted.".format(subdiv_code)}, 200
        return {'message': "Subdiv '{}' not found.".format(subdiv_code)}, 404


class SubdivList(Resource):
    @jwt_required
    def get(self):
        subdivs = [subdiv.json() for subdiv in SubdivModel.find_all()]
        return {'subdivs': subdivs}, 200
