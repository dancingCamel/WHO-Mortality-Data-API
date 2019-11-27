from flask_restful import Resource, reqparse
from models.icd10_lists import Icd10ListsModel
from auth import requireApiKey, requireAdmin


class Icd10CodeListCode(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @requireApiKey
    def get(self, code):
        code_list = Icd10ListsModel.find_by_code(code)
        if code_list:
            return code_list.json(), 200
        return {'message': "Code list '{}' not found.".format(code)}, 404

    @requireAdmin
    def post(self, code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        if Icd10ListsModel.find_by_code(code):
            return {'message': "List '{}' already exists.".format(code)}, 404

        data = Icd10CodeList.parser.parse_args()
        new_list = Icd10ListsModel(code, data['description'])
        try:
            new_list.save_to_db()
        except:
            {'message': "An error occurred inserting the list."}, 500
        return new_list.json()

    @requireAdmin
    def put(self, code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        code_list = Icd10ListsModel.find_by_code(code)

        data = Icd10CodeList.parser.parse_args()
        if code_list:
            code_list.description = data['description']
        else:
            code_list = Icd10ListsModel(code, data['description'])

        try:
            code_list.save_to_db()
        except:
            {'message': "An error occurred inserting the list."}, 500
        return code_list.json()

    @requireAdmin
    def delete(self, code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        code_list = Icd10ListsModel.find_by_code(code)
        if code_list:
            code_list.delete_from_db()
            return {'message': "List '{}' deleted.".format(code)}, 200
        return {'message': "List '{}' not found.".format(code)}, 404


class Icd10CodeListDesc(Resource):
    def get(self, search_term):
        lists = [icd10list.json()
                 for icd10list in Icd10ListsModel.search_by_desc(search_term)]
        if lists:
            return {'lists': lists}, 200
        return {'message': "No lists match that search term"}, 404


class Icd10AllCodeLists(Resource):
    # return all available code lists and their descritpion e.g. 101, 103, 104
    @requireApiKey
    def get(self):
        code_lists = [code_list.json()
                      for code_list in Icd10ListsModel.find_all()]
        return {'code_lists': code_lists}
