from flask_restful import Resource, reqparse
from models.sex import SexModel
from flask_jwt_extended import (
    jwt_required,
    fresh_jwt_required,
    get_jwt_claims
)


class Sex(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('sex_code',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @jwt_required
    def get(self, sex):
        sex_entry = SexModel.find_by_name(sex)
        if sex_entry:
            return sex_entry.json()
        return {'message': "Sex not found."}, 404

    @fresh_jwt_required
    def post(self, sex):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        data = Sex.parser.parse_args()
        if SexModel.find_by_name(sex):
            return {'message': "Sex '{}' already exists.".format(sex)}, 400

        entry = SexModel(sex, data['sex_code'])

        try:
            entry.save_to_db()
        except:
            return {'message': "An error occurred inserting the sex."}, 500
        return entry.json(), 201

    @fresh_jwt_required
    def put(self, sex):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        data = Sex.parser.parse_args()
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

    @fresh_jwt_required
    def delete(self, sex):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        entry = SexModel.find_by_name(sex)
        if entry:
            entry.delete_from_db()
            return {'message': "Sex '{}' deleted".format(sex)}, 200
        return {'message': "Sex '{}' not found.".format(sex)}, 404


class SexList(Resource):
    # return list of all sexes and their codes
    @jwt_required
    def get(self):
        sexes = [sex.json() for sex in SexModel.find_all()]
        return {'sexes': sexes}, 200
