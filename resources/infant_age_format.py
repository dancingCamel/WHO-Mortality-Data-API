from flask_restful import Resource, reqparse
from models.infant_age_format import InfantAgeFormatModel
from auth import requireApiKey, requireAdmin


class InfantAgeFormatCode(Resource):
    parser = reqparse.RequestParser()

    for num in range(1, 5):
        parser.add_argument('infantAge'+str(num),
                            type=str)

    @requireApiKey
    def get(self, infant_age_format_code):
        infant_age_format = InfantAgeFormatModel.find_by_code(
            infant_age_format_code)
        if infant_age_format:
            return infant_age_format.json(), 200
        return {'message': "No infant age format found with code '{}'.".format(infant_age_format_code)}, 404

    @requireAdmin
    def post(self, infant_age_format_code):
        data = InfantAgeFormatCode.parser.parse_args()
        infant_age_format = InfantAgeFormatModel.find_by_code(
            infant_age_format_code)
        if infant_age_format:
            return {'message': "An infant age format already exists with code '{}'".format(infant_age_format_code)}, 404
        infant_age_format = InfantAgeFormatModel(
            infant_age_format_code, **data)
        try:
            infant_age_format.save_to_db()
        except:
            return {'message', "An error occured inserting the infant age format"}, 500
        return infant_age_format.json(), 201

    @requireAdmin
    def put(self, infant_age_format_code):
        data = InfantAgeFormatCode.parser.parse_args()
        infant_age_format = InfantAgeFormatModel.find_by_code(
            infant_age_format_code)

        if infant_age_format:
            infant_age_format.infantAge1 = data['infantAge1']
            infant_age_format.infantAge2 = data['infantAge2']
            infant_age_format.infantAge3 = data['infantAge3']
            infant_age_format.infantAge4 = data['infantAge4']
        else:
            infant_age_format = InfantAgeFormatModel(
                infant_age_format_code, **data)
        try:
            infant_age_format.save_to_db()
        except:
            return {'message': "An error occurred inserting the infant age format."}, 500
        return infant_age_format.json(), 201

    @requireAdmin
    def delete(self, infant_age_format_code):
        infant_age_format = InfantAgeFormatModel.find_by_code(
            infant_age_format_code)
        if infant_age_format:
            infant_age_format.delete_from_db()
            return {'message': "Infant age format code '{}' deleted.".format(infant_age_format_code)}, 200
        return {'message': "Infant age format with code '{}' not found.".format(infant_age_format_code)}, 404


class InfantAgeFormatList(Resource):
    @requireApiKey
    def get(self):
        infant_age_formats = [infant_age_format.json(
        ) for infant_age_format in InfantAgeFormatModel.find_all()]
        return {'formats': infant_age_formats}, 200
