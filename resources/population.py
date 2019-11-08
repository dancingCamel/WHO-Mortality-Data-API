from flask_restful import Resource, request
from validate import *
from models.population import PopulationModel


class Population(Resource):
    # search for entries
    def get(self):
        # Validate request
        country_code = request.args.get('country_code', type=str)
        # if country_code:
        #     # check valid country_code
        #     validate_country_code(country_code)

        year = request.args.get('year', type=str)
        # if year:
        #     validate_year(year)

        sex = request.args.get('sex', type=str)
        # if sex:
        #     validate_sex(sex)
        query = {}
        if sex:
            query['sex'] = sex
        if country_code:
            query['country_code'] = country_code
        if year:
            query['year'] = year
        # query = {'country_code': country_code, 'year': year, 'sex': sex}
        results = [entry.json()
                   for entry in PopulationModel.search_populations(query)]

        # results = PopulationModel.query.filter_by(
        #     country_code=country_code).first()

        if results:
            return {'populations': results}
        return {'message': "No populations match your query."}, 404

    # use parser to ensure we have a value set for each of the 3 parameters

    def post(self):
        # need to have non default values for year sex and country - must be specific to one line in table
        # need to have values for all columns
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
