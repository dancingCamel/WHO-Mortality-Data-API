from flask_restful import Resource, reqparse
from models.icd_lists import IcdListsModel
from auth import requireApiKey, requireAdmin


class IcdCodeListCode(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @requireApiKey
    def get(self, code):
        code_list = IcdListsModel.find_by_code(code)
        if code_list:
            return code_list.json(), 200
        return {'message': "Code list '{}' not found.".format(code)}, 404

    @requireAdmin
    def post(self, code):
        if IcdListsModel.find_by_code(code):
            return {'message': "List '{}' already exists.".format(code)}, 404

        data = IcdCodeListCode.parser.parse_args()
        new_list = IcdListsModel(code, data['description'])
        try:
            new_list.save_to_db()
        except:
            {'message': "An error occurred inserting the list."}, 500
        return new_list.json()

    @requireAdmin
    def put(self, code):
        code_list = IcdListsModel.find_by_code(code)

        data = IcdCodeListCode.parser.parse_args()
        if code_list:
            code_list.description = data['description']
        else:
            code_list = IcdListsModel(code, data['description'])

        try:
            code_list.save_to_db()
        except:
            {'message': "An error occurred inserting the list."}, 500
        return code_list.json()

    @requireAdmin
    def delete(self, code):
        code_list = IcdListsModel.find_by_code(code)
        if code_list:
            code_list.delete_from_db()
            return {'message': "List '{}' deleted.".format(code)}, 200
        return {'message': "List '{}' not found.".format(code)}, 404


class IcdCodeListDesc(Resource):
    def get(self, search_term):
        lists = [icdlist.json()
                 for icdlist in IcdListsModel.search_by_desc(search_term)]
        if lists:
            return {'lists': lists}, 200
        return {'message': "No lists match that search term"}, 404


class IcdAllCodeLists(Resource):
    @requireApiKey
    def get(self):
        code_lists = [code_list.json()
                      for code_list in IcdListsModel.find_all()]
        return {'code_lists': code_lists}
