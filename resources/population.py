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
                        default="",
                        )

    parser.add_argument('subdiv',
                        type=str,
                        default="",
                        )

    parser.add_argument('age_format',
                        type=str,
                        default="00",
                        )

    parser.add_argument('live_births',
                        type=str,
                        default="",
                        )

    for num in range(1, 27):
        parser.add_argument('pop' + str(num),
                            type=str,
                            default=""
                            )

    # search for entries

    def get(self):
        query = {}
        # Validate request and add to query
        country_code = request.args.get('country', type=str)
        if country_code:
            if not valid_country_code(country_code):
                return {'message': '{} is not a valid country_code'.format(country_code)}, 400
            query['country_code'] = country_code

        year = request.args.get('year', type=str)
        if year:
            if not valid_year(year):
                return {'message': 'Please enter a valid year'}, 400
            query['year'] = year

        sex = request.args.get('sex', type=str)
        if sex:
            if not valid_sex(sex):
                return {'message': 'Please enter a valid sex code'}, 400
            query['sex'] = sex

        admin = request.args.get('admin', type=str)
        if admin:
            if not valid_admin(admin):
                return {'message': 'Please enter a valid admin code'}, 400
            query['admin'] = admin

        subdiv = request.args.get('subdiv', type=str)
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400
            query['subdiv'] = subdiv

        results = [entry.json()
                   for entry in PopulationModel.search_populations(query)]

        if results:
            return {'entries': results}
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
            entry[0].delete_from_db()
            return {'message': 'Entry deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self):
        data = Population.parser.parse_args()

        entry = PopulationModel.find_by_cysas(
            data['country_code'], data['year'], data['sex'], data['admin'], data['subdiv'])

        if entry:
            entry.age_format = data['age_format']
            entry.live_births = data['live_births']
            entry.pop1 = data['pop1']
            entry.pop2 = data['pop2']
            entry.pop3 = data['pop3']
            entry.pop4 = data['pop4']
            entry.pop5 = data['pop5']
            entry.pop6 = data['pop6']
            entry.pop7 = data['pop7']
            entry.pop8 = data['pop8']
            entry.pop9 = data['pop9']
            entry.pop10 = data['pop10']
            entry.pop11 = data['pop11']
            entry.pop12 = data['pop12']
            entry.pop13 = data['pop13']
            entry.pop14 = data['pop14']
            entry.pop15 = data['pop15']
            entry.pop16 = data['pop16']
            entry.pop17 = data['pop17']
            entry.pop18 = data['pop18']
            entry.pop19 = data['pop19']
            entry.pop20 = data['pop20']
            entry.pop21 = data['pop21']
            entry.pop22 = data['pop22']
            entry.pop23 = data['pop23']
            entry.pop24 = data['pop24']
            entry.pop25 = data['pop25']
            entry.pop26 = data['pop26']

        else:
            entry = PopulationModel(**data)

        # entry.save_to_db()
        return entry.json()


class PopulationOne(Resource):
    def get(self):
        query = {}
        # Validate request and add to query
        country_code = request.args.get('country', type=str)
        if country_code:
            if not valid_country_code(country_code):
                return {'message': '{} is not a valid country_code'.format(country_code)}, 400
            query['country_code'] = country_code

            year = request.args.get('year', type=str)
            if year:
                if not valid_year(year):
                    return {'message': 'Please enter a valid year'}, 400
                query['year'] = year

            sex = request.args.get('sex', type=str)
            if sex:
                if not valid_sex(sex):
                    return {'message': 'Please enter a valid sex code'}, 400
                query['sex'] = sex

            admin = request.args.get('admin', type=str)
            if admin:
                if not valid_admin(admin):
                    return {'message': 'Please enter a valid admin code'}, 400
                query['admin'] = admin

            subdiv = request.args.get('subdiv', type=str)
            if subdiv:
                if not valid_subdiv(subdiv):
                    return {'message': 'Please enter a valid subdiv code'}, 400
                query['subdiv'] = subdiv

            result = [entry.json()
                      for entry in PopulationModel.search_populations(query)]

            if result:
                if len(result) > 1:
                    return {'message': "More than one population entry was found matching your query."}, 400
                return {'entry': result[0]}, 200

            return {'message': "No populations match your query."}, 404


class PopulationsAll(Resource):
    # get all population data
    def get(self):
        populations = [entry.json() for entry in PopulationModel.find_all()]
        return {'populations': populations}, 200
