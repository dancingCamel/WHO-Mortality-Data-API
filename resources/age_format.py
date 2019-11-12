from flask_restful import Resource, reqparse
from models.age_format import AgeFormatModel


class AgeFormat(Resource):
    parser = reqparse.RequestParser()
    # add arguments with for loop like in population resource
    for num in range(2, 27):
        parser.add_argument('pop' + str(num),
                            type=str,
                            default="empty"+str(num)
                            )

    def get(self, age_format_code):
        format = AgeFormatModel.find_by_code(age_format_code)
        if format:
            return format.json()
        return {'message': "Age format {} not found".format(age_format_code)}, 404

    def post(self, age_format_code):
        data = AgeFormat.parser.parse_args()

        format = AgeFormatModel.find_by_code(age_format_code)
        if format:
            return {'message': "Age format {} already exists.".format(age_format_code)}, 400

        # this isn't working
        format = AgeFormatModel(age_format_code, **data)

        try:
            format.save_to_db()
        except:
            return {'message': "An error occurred inserting the age format."}, 500
        return format.json(), 201

    def put(self, age_format_code):
        data = AgeFormat.parser.parse_args()

        format = AgeFormatModel.find_by_code(age_format_code)

        if format:
            format.pop2 = data['pop2']
            format.pop3 = data['pop3']
            format.pop4 = data['pop4']
            format.pop5 = data['pop5']
            format.pop6 = data['pop6']
            format.pop7 = data['pop7']
            format.pop8 = data['pop8']
            format.pop9 = data['pop9']
            format.pop10 = data['pop10']
            format.pop11 = data['pop11']
            format.pop12 = data['pop12']
            format.pop13 = data['pop13']
            format.pop14 = data['pop14']
            format.pop15 = data['pop15']
            format.pop16 = data['pop16']
            format.pop17 = data['pop17']
            format.pop18 = data['pop18']
            format.pop19 = data['pop19']
            format.pop20 = data['pop20']
            format.pop21 = data['pop21']
            format.pop22 = data['pop22']
            format.pop23 = data['pop23']
            format.pop24 = data['pop24']
            format.pop25 = data['pop25']
            format.pop26 = data['pop26']
        else:
            format = AgeFormatModel(age_format_code, **data)

        try:
            format.save_to_db()
        except:
            return {'message': "An error occurred inserting the age format for code '{}'.".format(age_format_code)}, 500
        return format.json(), 201

    def delete(self, age_format_code):
        format = AgeFormatModel.find_by_code(age_format_code)
        if format:
            format.delete_from_db()
            return {'message': "Age format '{}' deleted.".format(age_format_code)}, 200
        return {'message': "Age format '{}' not found.".format(age_format_code)}, 404


class AgeFormatList(Resource):
    def get(self):
        formats = [format.json() for format in AgeFormatModel.find_all()]
        return {'formats': formats}, 200
