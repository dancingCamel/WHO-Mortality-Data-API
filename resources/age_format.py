from flask import jsonify, json
from flask_restful import Resource, reqparse
from models.age_format import AgeFormatModel
from auth import requireApiKey, requireAdmin


class AgeFormat(Resource):
    parser = reqparse.RequestParser()
    # add arguments with for loop like in population resource
    for num in range(2, 27):
        parser.add_argument('pop' + str(num),
                            type=str,
                            default="empty"+str(num)
                            )

    @requireApiKey
    def get(self, age_format_code):
        age_format = AgeFormatModel.find_by_code(age_format_code)
        if age_format:
            return json.dumps(age_format.json())
        return {'message': "Age format {} not found".format(age_format_code)}, 404

    @requireAdmin
    def post(self, age_format_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        data = AgeFormat.parser.parse_args()

        age_format = AgeFormatModel.find_by_code(age_format_code)
        if age_format:
            return {'message': "Age format {} already exists.".format(age_format_code)}, 400

        age_format = AgeFormatModel(age_format_code, **data)

        try:
            age_format.save_to_db()
        except:
            return {'message': "An error occurred inserting the age format."}, 500
        return age_format.json(), 201

    @requireAdmin
    def put(self, age_format_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        data = AgeFormat.parser.parse_args()

        age_format = AgeFormatModel.find_by_code(age_format_code)

        if age_format:
            age_format.pop2 = data['pop2']
            age_format.pop3 = data['pop3']
            age_format.pop4 = data['pop4']
            age_format.pop5 = data['pop5']
            age_format.pop6 = data['pop6']
            age_format.pop7 = data['pop7']
            age_format.pop8 = data['pop8']
            age_format.pop9 = data['pop9']
            age_format.pop10 = data['pop10']
            age_format.pop11 = data['pop11']
            age_format.pop12 = data['pop12']
            age_format.pop13 = data['pop13']
            age_format.pop14 = data['pop14']
            age_format.pop15 = data['pop15']
            age_format.pop16 = data['pop16']
            age_format.pop17 = data['pop17']
            age_format.pop18 = data['pop18']
            age_format.pop19 = data['pop19']
            age_format.pop20 = data['pop20']
            age_format.pop21 = data['pop21']
            age_format.pop22 = data['pop22']
            age_format.pop23 = data['pop23']
            age_format.pop24 = data['pop24']
            age_format.pop25 = data['pop25']
            age_format.pop26 = data['pop26']
        else:
            age_format = AgeFormatModel(age_format_code, **data)

        try:
            age_format.save_to_db()
        except:
            return {'message': "An error occurred inserting the age format for code '{}'.".format(age_format_code)}, 500
        return age_format.json(), 201

    @requireAdmin
    def delete(self, age_format_code):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        age_format = AgeFormatModel.find_by_code(age_format_code)
        if age_format:
            age_format.delete_from_db()
            return {'message': "Age format '{}' deleted.".format(age_format_code)}, 200
        return {'message': "Age format '{}' not found.".format(age_format_code)}, 404


class AgeFormatList(Resource):
    @requireApiKey
    def get(self):
        age_formats = [age_format.json()
                       for age_format in AgeFormatModel.find_all()]
        return {'formats': age_formats}, 200
