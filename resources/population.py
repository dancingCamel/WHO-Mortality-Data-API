from flask_restful import Resource, request, reqparse
from validate import *
from models.population import PopulationModel


class Population(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('country_code',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    parser.add_argument('sex',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    parser.add_argument('year',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    parser.add_argument('admin',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    parser.add_argument('subdiv',
                        type=str,
                        required=True,
                        help="This field is required"
                        )

    parser.add_argument('age_format',
                        type=str,
                        help="This field is required"
                        )

    parser.add_argument('live_births',
                        type=str,
                        help="This field is required"
                        )

    for num in range(1, 27):
        parser.add_argument('pop' + str(num),
                            type=str
                            )

    # search for entries

    def get(self):
        # Validate request
        country_code = request.args.get('country_code', type=str)
        if country_code:
            if not valid_country_code(country_code):
                return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        year = request.args.get('year', type=str)
        if year:
            if not valid_year(year):
                return {'message': 'Please enter a valid year'}, 400

        sex = request.args.get('sex', type=str)
        if sex:
            if not valid_sex(sex):
                return {'message': 'Please enter a valid sex code'}, 400

        admin = request.args.get('admin', type=str)
        if admin:
            if not valid_admin(admin):
                return {'message': 'Please enter a valid admin code'}, 400

        subdiv = request.args.get('subdiv', type=str)
        # if subdiv:
        # if not valid_subdiv(subdiv):
        # return {'message': 'Please enter a valid subdiv code'}, 400

        query = {}
        if sex:
            query['sex'] = sex
        if country_code:
            query['country_code'] = country_code
        if year:
            query['year'] = year
        if admin:
            query['admin'] = admin
        if subdiv:
            query['subdiv'] = subdiv

        results = [entry.json()
                   for entry in PopulationModel.search_populations(query)]

        if results:
            return {'populations': results}
        return {'message': "No populations match your query."}, 404

    # use parser to ensure we have a value set for each of the 3 parameters

    def post(self):
        # need to have non default values for year sex and country - must be specific to one line in table
        # if find multiple entries for given ASC, return what's given and ask users to add admin or subdiv as required to choose only one
        data = Population.parser.parse_args()
        # check to see if entry already exists given all parameters
        if PopulationModel.find_by_cysas(data['country_code'], data['year'], data['sex'], data['admin'], data['subdiv']):
            return {'message': "An entry already exists for your given year, country, sex, admin and subdiv."}, 400

        entry = PopulationModel(**data)

        try:
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return entry.json(), 201

    def delete(self):
        data = Population.parser.parse_args()

        entry = PopulationModel.find_by_cysas(
            data['country_code'], data['year'], data['sex'], data['admin'], data['subdiv'])

        if entry:
            if len(entry) > 1:
                return {'message': "More than one entry for given country, year and sex. Please specify one by adding an admin or subdiv according to the data below.",
                        'entries': [entry.json for entry in PopulationModel.find_by_cys(data['country_code'], data['year'], data['sex'])]}

            entry[0].delete_from_db()
            return {'message': 'Entry deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self):
        data = Population.parser.parse_args()

        if len(PopulationModel.find_by_cys(data['country_code'], data['year'], data['sex'])) > 1:
            return {'message': "More than one entry for given country, year and sex. Please specify one by adding an admin or subdiv according to the data below.",
                    'entries': [entry.json for entry in PopulationModel.find_by_cys(data['country_code'], data['year'], data['sex'])]}


class PopulationsAll(Resource):
    # get all population data
    def get(self):
        populations = [entry.json() for entry in PopulationModel.find_all()]
        return {'populations': populations}, 200
