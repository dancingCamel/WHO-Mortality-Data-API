from flask_restful import Resource, reqparse
from models.country import CountryModel
from sqlalchemy import func
from flask_login import login_required
from auth import requireApiKey, requireAdmin


class CountryCode(Resource):
    @requireApiKey
    # get the country name when supplying a country code
    def get(self, country_code):
        country = CountryModel.find_by_code(country_code)
        if country:
            return country.json(), 200
        return {'message': "Country -'{}'- not found.".format(country_code)}, 404


class CountryName(Resource):
    # assuming we know the name of the country but don't know its Country Code
    parser = reqparse.RequestParser()
    parser.add_argument('country_code',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    @requireApiKey
    # get the country code when supplying a country name
    def get(self, country_name):
        country = CountryModel.find_by_name(country_name)
        if country:
            return country.json(), 200
        return {'message': "Country -'{}'- not found.".format(country_name)}, 404

    # add a new country code and name - check code doesn't already exist
    @requireAdmin
    def post(self, country_name):
        if CountryModel.find_by_name(country_name):
            return {'message': "A country with name '{}' already exists.".format(country_name)}, 400

        data = Country.parser.parse_args()

        if CountryModel.find_by_code(data['country_code']):
            return {'message': "A country with code '{}' already exists.".format(data['country_code'])}, 400

        country = CountryModel(data['country_code'], country_name)

        try:
            country.save_to_db()
        except:
            return {'message': "An error occurred inserting the country."}, 500
        return country.json(), 201

    @requireAdmin
    # change code of given country
    def put(self, country_name):
        data = Country.parser.parse_args()
        country = CountryModel.find_by_name(country_name)

        if country:
            country.country_code = data['country_code']
        else:
            country = CountryModel(data['country_code'], country_name)

        country.save_to_db()
        return country.json()

    @requireAdmin
    def delete(self, country_name):
        country = CountryModel.find_by_name(country_name)
        if country:
            country.delete_from_db()
            return {'message': "Country '{}' deleted".format(country_name)}, 200
        return {'message': "Country '{}' not found.".format(country_name)}, 404


class CountryDesc(Resource):
    @requireApiKey
    def get(self, search_term):
        countries = [country.json()
                     for country in CountryModel.search_by_name(search_term)]
        if countries:
            return {'countries': countries}, 200
        return {'message': "No countries match that search term"}, 404


class CountryList(Resource):
    # return list of all countries and their codes
    @requireApiKey
    def get(self):
        countries = [country.json() for country in CountryModel.find_all()]
        return {'countries': countries}, 200


class CountrySearch(Resource):
    @requireApiKey
    def get(self, search_term):
        countries = [country.json()
                     for country in CountryModel.search_by_name(search_term)]
        if countries:
            return {'countries': countries}, 200
        return {'message': "No countries match that search term"}, 404
