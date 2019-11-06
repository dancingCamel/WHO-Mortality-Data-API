from flask_restful import Resource, reqparse
from models.country import CountryModel


class Country(Resource):
    # assuming we know the name of the country but don't know its Country Code
    # parser
    parser = reqparse.RequestParser()
    parser.add_argument('country_code',
                        type=str,
                        required=True,
                        help="This field is required"
                        )
    parser.add_argument('country_name',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    # get the country code when supplying a country name
    def get(self, country_name):
        country = CountryModel.find_by_name(country_name)
        if country:
            return country.json(), 200
        return {'message': "Country -'{}'- not found.".format(country_name)}, 404

    # post a country code when supplying a country name
    def post(self, country_name):
        pass

    # put a country code when supplying a country name
    def put(self, country_name):
        pass

    def delete(self, country_name):
        pass


class CountryList(Resource):
    # return list of all countries and their codes
    def get(self):
        countries = [country.json() for country in CountryModel.find_all()]
        return {'countries': countries}, 200
