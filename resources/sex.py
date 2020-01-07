from flask_restful import Resource, reqparse
from models.sex import SexModel
from auth import requireApiKey, requireAdmin


class SexCode(Resource):
    @requireApiKey
    def get(self, sex_code):
        sex_entry = SexModel.find_by_code(sex_code)
        if sex_entry:
            return sex_entry.json()
        return {'message': "Sex not found."}, 404


class SexDesc(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sex_code',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @requireApiKey
    def get(self, sex):
        sex_entry = SexModel.find_by_name(sex)
        if sex_entry:
            return sex_entry.json()
        return {'message': "Sex not found."}, 404

    @requireAdmin
    def post(self, sex):
        data = SexDesc.parser.parse_args()
        if SexModel.find_by_name(sex):
            return {'message': "Sex '{}' already exists.".format(sex)}, 400

        entry = SexModel(sex, data['sex_code'])

        try:
            entry.save_to_db()
        except:
            return {'message': "An error occurred inserting the sex."}, 500
        return entry.json(), 201

    @requireAdmin
    def put(self, sex):
        data = SexDesc.parser.parse_args()
        entry = SexModel.find_by_name(sex)

        if entry:
            entry.sex_code = data['sex_code']
        else:
            entry = SexModel(sex, data['sex_code'])

        try:
            entry.save_to_db()
        except:
            return {'message': "An error occurred inserting the sex."}, 500
        return entry.json(), 201

    @requireAdmin
    def delete(self, sex):
        entry = SexModel.find_by_name(sex)
        if entry:
            entry.delete_from_db()
            return {'message': "Sex '{}' deleted".format(sex)}, 200
        return {'message': "Sex '{}' not found.".format(sex)}, 404


class SexList(Resource):
    @requireApiKey
    def get(self):
        sexes = [sex.json() for sex in SexModel.find_all()]
        return {'sexes': sexes}, 200
