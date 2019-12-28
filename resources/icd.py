from flask_restful import Resource, reqparse
from models.icd import IcdModel
from auth import requireApiKey, requireAdmin


class Icd(Resource):
    # look for specific ICD entry given code_list and code
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required")

    @requireApiKey
    def get(self, code_list, code):
        entry = IcdModel.find_by_list_and_code(code_list, code)
        if entry:
            return entry.json(), 200
        return {'message': "'{}' code not found in the '{}' list.".format(code, code_list)}, 404

    @requireAdmin
    def post(self, code_list, code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        if IcdModel.find_by_list_and_code(code_list, code):
            return {'message': "A '{}' code already exists in list '{}'.".format(code, code_list)}, 400

        data = Icd.parser.parse_args()

        entry = IcdModel(code_list, code, data['description'])

        try:
            entry.save_to_db()
        except:
            return {'message': "Something we wrong inserting the code."}, 500
        return entry.json(), 201

    @requireAdmin
    def put(self, code_list, code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        entry = IcdModel.find_by_list_and_code(code_list, code)

        data = Icd.parser.parse_args()
        if entry:
            entry.description = data['description']
        else:
            entry = IcdModel(code_list, code, data['description'])

        try:
            entry.save_to_db()
        except:
            return {'message': "Something we wrong inserting the code."}, 500
        return entry.json(), 201

    @requireAdmin
    def delete(self, code_list, code):
        entry = IcdModel.find_by_list_and_code(code_list, code)
        if entry:
            entry.delete_from_db()
            return {'message': "Deleted code '{}' from list '{}'.".format(code, code_list)}, 200
        return {'message': "Code '{}' not found in list '{}'.".format(code, code_list)}, 404


class IcdCode(Resource):
    # get all codes that match a code (list code pairs)
    @requireApiKey
    def get(self, code):
        code = code.upper()
        entries = IcdModel.find_by_code(code)
        if entries:
            return {'results': [entry.json() for entry in entries]}, 200
        return {'message': "No results match the code '{}'.".format(code)}, 404


class IcdDesc(Resource):
    # search for codes using a case insensitive partial description or code
    @requireApiKey
    def get(self, search_term):
        if len(search_term) < 3:
            return {'message': "Please search for a term at least 3 characters long."}, 400
        entries = IcdModel.search(search_term)
        if entries:
            return {'results': [entry.json() for entry in entries]}, 200
        return {'message': "No results match the search term '{}'.".format(search_term)}, 404


class IcdSearch(Resource):
    # search for codes using a case insensitive partial description or code
    @requireApiKey
    def get(self, search_term):
        entries = IcdModel.search(search_term)
        if entries:
            return {'results': [entry.json() for entry in entries]}, 200
        return {'message': "No results match the search term '{}'.".format(search_term)}, 404


class IcdList(Resource):
    # return whole icd list in json format
    @requireApiKey
    def get(self):
        entries = [entry.json() for entry in IcdModel.find_all()]
        return {'all_codes': entries}
