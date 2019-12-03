from flask_restful import Resource, reqparse
from models.subdiv import SubdivModel
from auth import requireApiKey, requireAdmin


class SubdivCode(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required")

    @requireApiKey
    def get(self, subdiv_code):
        subdiv = SubdivModel.find_by_code(subdiv_code)
        if subdiv:
            return subdiv.json()
        return {'message': "Subdiv {} not found".format(subdiv_code)}, 404

    @requireAdmin
    def post(self, subdiv_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
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

    @requireAdmin
    def put(self, subdiv_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
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

    @requireAdmin
    def delete(self, subdiv_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        subdiv = SubdivModel.find_by_code(subdiv_code)

        if subdiv:
            subdiv.delete_from_db()
            return {'message': "Subdiv '{}' deleted.".format(subdiv_code)}, 200
        return {'message': "Subdiv '{}' not found.".format(subdiv_code)}, 404


class SubdivDesc(Resource):
    # search description endpoint for use in Code page
    @requireApiKey
    def get(self, search_term):
        subdivs = [subdiv.json()
                   for subdiv in SubdivModel.search_by_desc(search_term)]
        if subdivs:
            return {'subdivs': subdivs}, 200
        return {'message': "No subdivs match that search term"}, 404


class SubdivList(Resource):
    @requireApiKey
    def get(self):
        subdivs = [subdiv.json() for subdiv in SubdivModel.find_all()]
        return {'subdivs': subdivs}, 200


class SubdivSearch(Resource):
    # search endpoint for use in JSON and Visualise pages
    @requireApiKey
    def get(self, search_term):
        subdivs = [subdiv.json()
                   for subdiv in SubdivModel.search_by_desc(search_term)]
        if subdivs:
            return {'results': subdivs}, 200
        return {'message': "No subdivs match that search term"}, 404
