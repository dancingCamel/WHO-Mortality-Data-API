from flask_restful import Resource, reqparse
from models.admin import AdminModel


class Admin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @jwt_required
    def get(self, admin_code, country_code):
        admin = AdminModel.find_by_code_and_country(admin_code, country_code)
        if admin:
            return admin.json()
        return {'message': "No admin entry found for code {} and country {}.".format(admin_code, country_code)}, 404

    @fresh_jwt_required
    def post(self, admin_code, country_code):
        data = Admin.parser.parse_args()

        if AdminModel.find_by_code_and_country(admin_code, country_code):
            return {'message': "A '{}' admin code already exists for country with code '{}'.".format(admin_code, country_code)}, 400

        entry = AdminModel(admin_code, country_code, data['description'])
        try:
            entry.save_to_db()
        except:
            {'message': 'Something went wrong inserting the admin.'}, 500
        return entry.json(), 201

    @fresh_jwt_required
    def put(self, admin_code, country_code):
        data = Admin.parser.parse_args()

        entry = AdminModel.find_by_code_and_country(admin_code, country_code)

        if entry:
            entry.description = data['description']
        else:
            entry = AdminModel(admin_code, country_code, data['description'])
        try:
            entry.save_to_db()
        except:
            {'message': 'Something went wrong inserting the admin.'}, 500
        return entry.json(), 201

    @fresh_jwt_required
    def delete(self, admin_code, country_code):
        entry = AdminModel.find_by_code_and_country(admin_code, country_code)

        if entry:
            entry.delete_from_db()
            return {'message': "Admin code '{}' for country code '{}' deleted.".format(admin_code, country_code)}, 200
        return {'message': "Admin code '{}' not found for country with code '{}'.".format(admin_code, country_code)}, 404


class AdminList(Resource):
    @jwt_required
    def get(self):
        admins = AdminModel.find_all()
        return [entry.json() for entry in admins], 200
