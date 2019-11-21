from flask_restful import Resource, reqparse
from models.icd10 import Icd10Model


class Icd10(Resource):
    # look for specific ICD10 entry given code_list and code
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required")

    @jwt_required
    def get(self, code_list, code):
        entry = Icd10Model.find_by_list_and_code(code_list, code)
        if entry:
            return entry.json(), 200
        return {'message': "'{}' code not found in the '{}' list.".format(code, code_list)}, 404

    @fresh_jwt_required
    def post(self, code_list, code):
        if Icd10Model.find_by_list_and_code(code_list, code):
            return {'message': "A '{}' code already exists in list '{}'.".format(code, code_list)}, 400

        data = Icd10.parser.parse_args()

        entry = Icd10Model(code_list, code, data['description'])

        try:
            entry.save_to_db()
        except:
            return {'message': "Something we wrong inserting the code."}, 500
        return entry.json(), 201

    @fresh_jwt_required
    def put(self, code_list, code):
        entry = Icd10Model.find_by_list_and_code(code_list, code)

        data = Icd10.parser.parse_args()
        if entry:
            entry.description = data['description']
        else:
            entry = Icd10Model(code_list, code, data['description'])

        try:
            entry.save_to_db()
        except:
            return {'message': "Something we wrong inserting the code."}, 500
        return entry.json(), 201

    @fresh_jwt_required
    def delete(self, code_list, code):
        entry = Icd10Model.find_by_list_and_code(code_list, code)
        if entry:
            entry.delete_from_db()
            return {'message': "Deleted code '{}' from list '{}'.".format(code, code_list)}, 200
        return {'message': "Code '{}' not found in list '{}'.".format(code, code_list)}, 404


class Icd10Search(Resource):
    # search for codes using a case insensitive partial description or code
    @jwt_required
    def get(self, search_term):
        entries = Icd10Model.search(search_term)
        if entries:
            return {'results': [entry.json() for entry in entries]}, 200
        return {'message': "No results match the search term '{}'.".format(search_term)}, 404


class Icd10List(Resource):
    # return whole icd10 list in json format
    @jwt_required
    def get(self):
        entries = [entry.json() for entry in Icd10Model.find_all()]
        return {'all_codes': entries}
