from flask_restful import Resource, request
from models.population import PopulationModel
from models.country import CountryModel


class Population(Resource):
    # search for entries
    # no parser required as just searching
    def get(self):
        # accept url parameters year, sex, country. any combination (if not specified then select all)
        # get working for one variable first, then all 3 variables at same time. then allow multiple of each variable

        country = request.args.get('country', default='*', type=str)
        # try to convert to integer, if can do it then it's a code. if can't then its a country name and we need to find the code
        try:
            int(country)
        except:
            global country
            country = CountryModel.find_by_name(country).country_code

        sex = request.args.get('sex', default='*', type=str)
        # try to convert to integer, if can then it's a code. if can't then we need to convert it to a code

        year = request.args.get('year', default='*', type=str)

        return

    # use parser to ensure we have a value set for each of the 3 parameters

    def post(self):
        # need to have non default values for year sex and country - must be specific to one line in table
        pass

    # use parser to ensure we have a value set for each of the 3 parameters
    def delete(self):
        # need to have non default values for year sex and country - must be specific to one line in table
        pass

        # use parser
    def put(self):
        # need to have non default values for year sex and country - must be specific to one line in table (one year, one sex, one country)
        pass


class PopulationsAll(Resource):
    # get all population data
    def get(self):
        pass
