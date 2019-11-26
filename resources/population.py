from flask_restful import Resource, request, reqparse
from validate import *
from models.population import PopulationModel
from auth import requireApiKey, requireAdmin


class PopulationSearch(Resource):
    # search for entries
    @requireApiKey
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


class PopulationChange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('admin',
                        type=str,
                        )

    parser.add_argument('subdiv',
                        type=str,
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

    @requireAdmin
    def post(self, country_code, year, sex):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        # need to add new country to countries list and new admin/subdiv to admin/subdiv lists before adding new population entry using those codes
        data = PopulationChange.parser.parse_args()

        # validation
        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        # post_format tells us if we have an admin or subdiv code while allowing us to change their values
        post_format = [0, 0]
        admin = data['admin']
        if admin:
            if not valid_admin(admin):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            # delete null value from data object
            del data['admin']

        subdiv = data['subdiv']
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1
            del data['subdiv']

        # if have admin and subdiv
        if post_format[0] == 1 and post_format[1] == 1:
            if PopulationModel.find_by_cysas(country_code, year, sex, admin, subdiv):
                return {'message': "An entry already exists for your given year, country, sex, admin and subdiv."}, 400

        # if have admin
        if post_format[0] == 1 and post_format[1] == 0:
            if PopulationModel.find_by_cysa(country_code, year, sex, admin):
                return {'message': "An entry already exists for your given year, country, sex and admin."}, 400
            subdiv = ""
            # delete the null values from the data object
            del data['subdiv']

        # if have subdiv
        if post_format[0] == 0 and post_format[1] == 1:
            if PopulationModel.find_by_cyss(country_code, year, sex, subdiv):
                return {'message': "An entry already exists for your given year, country, sex and subdiv."}, 400
            admin = ""
            del data['admin']

        # if have neither admin or data
        if post_format[0] == 0 and post_format[1] == 0:
            if PopulationModel.find_by_cys(country_code, year, sex):
                return {'message': "An entry already exists for your given year, country, sex."}, 400
            del data['admin']
            admin = ""
            del data['subdiv']
            subdiv = ""

        entry = PopulationModel(country_code, admin, subdiv, year, sex, **data)

        try:
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return entry.json(), 201

    @requireAdmin
    def delete(self, country_code, year, sex):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        data = PopulationChange.parser.parse_args()

        # validation
        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        # post_format tells us if we have an admin or subdiv code
        post_format = [0, 0]
        admin = data['admin']
        if admin:
            if not valid_admin(admin):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            # delete null value from data object

        subdiv = data['subdiv']
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1

        # if have admin and subdiv
        if post_format[0] == 1 and post_format[1] == 1:
            entry = PopulationModel.find_by_cysas(
                country_code, year, sex, admin, subdiv)

        # if have admin
        if post_format[0] == 1 and post_format[1] == 0:
            entry = PopulationModel.find_by_cysa(
                country_code, year, sex, admin)

        # if have subdiv
        if post_format[0] == 0 and post_format[1] == 1:
            entry = PopulationModel.find_by_cyss(
                country_code, year, sex, subdiv)

        # if have neither admin or data
        if post_format[0] == 0 and post_format[1] == 0:
            entry = PopulationModel.find_by_cys(country_code, year, sex)

        if entry:
            if len(entry) > 1:
                return {'message': "More than one population entry was found with the given parameters. Please supply either an admin or subdiv code as required.",
                        'entries': [population.json() for population in entry]}, 400
            entry[0].delete_from_db()
            return {'message': 'Entry deleted.'}
        return {'message': 'Item not found.'}, 404

    @requireAdmin
    def put(self, country_code, year, sex):
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return {'message': 'Admin privilege required'}, 401
        data = PopulationChange.parser.parse_args()

        # validation
        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        # post_format tells us if we have an admin or subdiv code
        post_format = [0, 0]
        admin = data['admin']
        if admin:
            if not valid_admin(admin):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            del data['admin']

        subdiv = data['subdiv']
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1
            del data['subdiv']

        # if have admin and subdiv
        if post_format[0] == 1 and post_format[1] == 1:
            entry = PopulationModel.find_by_cysas(
                country_code, year, sex, admin, subdiv)

        # if have admin
        if post_format[0] == 1 and post_format[1] == 0:
            entry = PopulationModel.find_by_cysa(
                country_code, year, sex, admin)

        # if have subdiv
        if post_format[0] == 0 and post_format[1] == 1:
            entry = PopulationModel.find_by_cyss(
                country_code, year, sex, subdiv)

        # if have neither admin or data
        if post_format[0] == 0 and post_format[1] == 0:
            entry = PopulationModel.find_by_cys(country_code, year, sex)

        if entry:
            entry.age_format = data['age_format']
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
            entry.live_births = data['live_births']

        else:
            entry = PopulationModel(
                country_code, admin, subdiv, year, sex, **data)

        entry.save_to_db()
        return entry.json()


class PopulationOne(Resource):
    @requireApiKey
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


class PopulationsList(Resource):
    # get all population data
    @requireApiKey
    def get(self):
        populations = [entry.json() for entry in PopulationModel.find_all()]
        return {'populations': populations}, 200
