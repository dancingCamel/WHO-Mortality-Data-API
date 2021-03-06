from flask_restful import Resource, reqparse, request
from models.mortality import MortalityDataModel
from models.code_list_ref import CodeListRefModel
from models.icd import IcdModel
from validate import *
import re
from auth import requireApiKey, requireAdmin


def strip_whitespace(string):
    return ('').join(string.split(' '))


class MortalityDataSearch(Resource):
    @requireApiKey
    def get(self):
        query = {}

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
            query['admin_code'] = admin

        subdiv = request.args.get('subdiv', type=str)
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400
            query['subdiv_code'] = subdiv

        cause = request.args.get('cause', type=str)
        if cause:
            cause_upper = cause.upper()
            if not valid_cause(cause_upper):
                return {'message': 'Please enter a valid cause code'}, 400

            cause_code_list_extended = {}

            icd_codes = [code.json()
                         for code in IcdModel.find_by_code(cause_upper)]
            for icd_code in icd_codes:

                matching_codes = [matching_icd_code.json()
                                  for matching_icd_code in IcdModel.search_specific(icd_code['description'])]
            unspecified_codes = []
            generic_codes = []

            pattern = "unspecified"
            match = re.search(pattern, icd_code['description'])
            if not match:
                unspecified_code = icd_code['description'] + \
                    " (unspecified)"
                unspecified_codes = [matching_icd_code.json(
                ) for matching_icd_code in IcdModel.search_specific(unspecified_code)]
            else:

                position = match.span()
                start = position[0] - 2
                end = position[1] + 1

                generic_code = icd_code['description'][0:start] + \
                    icd_code['description'][end:]
                generic_codes = [matching_icd_code.json(
                ) for matching_icd_code in IcdModel.search_specific(generic_code)]

            for matching_code in matching_codes:
                cause_code_list_extended[matching_code['list']
                                         ] = matching_code['code']

            if generic_codes:
                for matching_code in generic_codes:
                    cause_code_list_extended[matching_code['list']
                                             ] = matching_code['code']
            if unspecified_codes:
                for matching_code in unspecified_codes:
                    cause_code_list_extended[matching_code['list']
                                             ] = matching_code['code']

            if "103" not in cause_code_list_extended:
                try:
                    cause_code_list_extended['103'] = cause_code_list_extended['104'][:-1]
                except:
                    pass

            code_list_entry = CodeListRefModel.find_by_year_and_country(
                year, country_code)

            try:
                cause = cause_code_list_extended[code_list_entry.code_list]
            except:
                return {'message': "Can't find matching cause code for the specified country."}, 400

            query['cause'] = cause

        results = []
        results = [entry.json()
                   for entry in MortalityDataModel.search_mortalities(query)]

        if cause and code_list_entry.code_list == "104" and len(cause_code_list_extended[code_list_entry.code_list]) == 3:
            cause = cause + "9"
            query['cause'] = cause
            extra_result = [entry.json()
                            for entry in MortalityDataModel.search_mortalities(query)]
            for row in extra_result:
                results.append(row)

        if cause and code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 3:
            cause = cause + "9"
            query['cause'] = cause
            extra_result = [entry.json()
                            for entry in MortalityDataModel.search_mortalities(query)]
            for row in extra_result:
                results.append(row)

        if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 4:
            cause = cause[:-1]
            query['cause'] = cause
            extra_result = [entry.json()
                            for entry in MortalityDataModel.search_mortalities(query)]
            for row in extra_result:
                results.append(row)

        if results:
            return {'entries': results}, 200
        return {'message': "No mortality entries match your query."}, 404


class MortalitySearchMultiple(Resource):

    @requireApiKey
    def get(self):

        country_code_input = request.args.get('country', type=str)
        year_input = request.args.get('year', type=str)
        sex_code_input = request.args.get('sex', type=str)
        cause_code_input = request.args.get('cause', type=str)
        admin_code_input = request.args.get('admin', type=str)
        subdiv_code_input = request.args.get('subdiv', type=str)

        if not country_code_input or not year_input or not sex_code_input or not cause_code_input:
            return {'message': "Please add at least a year, country, sex and cause variable"}, 400

        country_code_list = strip_whitespace(country_code_input).split(',')
        year_list = strip_whitespace(year_input).split(',')
        sex_code_list = strip_whitespace(sex_code_input).split(',')
        cause_code_list = strip_whitespace(cause_code_input).split(',')

        cause_code_list = list(map(
            lambda x: x.upper(), cause_code_list))

        cause_code_list_extended = {}
        for icd_code in filter(valid_cause, cause_code_list):

            complete_icd_codes = [code.json()
                                  for code in IcdModel.find_by_code(icd_code)]

            for icd_code in complete_icd_codes:
                matching_codes = [matching_icd_code.json()
                                  for matching_icd_code in IcdModel.search_specific(icd_code['description'])]
                # try to make it possible to compare countries that use different code lists
                # check if contains "unspecified". if not, add it and search again. else remove "(unspecified)"
                # TODO: in case that unspecified doesn't match. sum up all instances of code + extra digit.
                # e.g. A02 input by user. if code list is 104, sum all A020, A021, ...A029. return sum
                # TODO: if user input is 4 digit cause code, remove last digit and search for 103 code list with that
                unspecified_codes = []
                generic_codes = []

                pattern = "unspecified"
                match = re.search(pattern, icd_code['description'])
                if not match:
                    unspecified_code = icd_code['description'] + \
                        " (unspecified)"
                    unspecified_codes = [matching_icd_code.json(
                    ) for matching_icd_code in IcdModel.search_specific(unspecified_code)]
                else:

                    position = match.span()
                    start = position[0] - 2
                    end = position[1] + 1

                    generic_code = icd_code['description'][0:start] + \
                        icd_code['description'][end:]
                    generic_codes = [matching_icd_code.json(
                    ) for matching_icd_code in IcdModel.search_specific(generic_code)]

                for matching_code in matching_codes:
                    cause_code_list_extended[matching_code['list']
                                             ] = matching_code['code']

                if generic_codes:
                    for matching_code in generic_codes:
                        cause_code_list_extended[matching_code['list']
                                                 ] = matching_code['code']
                if unspecified_codes:
                    for matching_code in unspecified_codes:
                        cause_code_list_extended[matching_code['list']
                                                 ] = matching_code['code']

                if "103" not in cause_code_list_extended:
                    try:
                        cause_code_list_extended['103'] = cause_code_list_extended['104'][:-1]
                    except:
                        pass

        # add "" to admin and subdiv lists to ensure some results if no specific code given
        admin_code_list = []
        if admin_code_input:
            admin_code_list = strip_whitespace(admin_code_input).split(',')
        admin_code_list.append("")

        subdiv_code_list = []
        if subdiv_code_input:
            subdiv_code_list = strip_whitespace(subdiv_code_input).split(',')
        subdiv_code_list.append("")

        # TODO: replace nested for loops with product function? - itertools.product or from itertools import product
        # def product(*args, **kwds):
        #     # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        #     # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        #     pools = map(tuple, args) * kwds.get('repeat', 1)
        #     result = [[]]
        #     for pool in pools:
        #         result = [x+[y] for x in result for y in pool]
        #     for prod in result:
        #         yield tuple(prod)

        results = []

        for country_code in filter(valid_country_code, country_code_list):
            for year in filter(valid_year, year_list):
                for sex in filter(valid_sex, sex_code_list):
                    for cause in filter(valid_cause, cause_code_list):
                        for admin in filter(valid_admin, admin_code_list):
                            for subdiv in filter(valid_subdiv, subdiv_code_list):

                                code_list_entry = CodeListRefModel.find_by_year_and_country(
                                    year, country_code)

                                try:
                                    cause = cause_code_list_extended[code_list_entry.code_list]
                                except:
                                    continue

                                query = {}
                                query['country_code'] = country_code
                                query['sex'] = sex
                                query['year'] = year
                                query['cause'] = cause
                                query['admin_code'] = admin
                                query['subdiv_code'] = subdiv

                                result = [entry.json()
                                          for entry in MortalityDataModel.search_mortalities(query)]

                                if code_list_entry.code_list == "104" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(result) == 0:
                                    cause = cause + "9"
                                    query['cause'] = cause
                                    result = [entry.json()
                                              for entry in MortalityDataModel.search_mortalities(query)]

                                if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(result) == 0:
                                    cause = cause + "9"
                                    query['cause'] = cause
                                    result = [entry.json()
                                              for entry in MortalityDataModel.search_mortalities(query)]

                                if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 4 and len(result) == 0:
                                    cause = cause[:-1]
                                    query['cause'] = cause
                                    result = [entry.json()
                                              for entry in MortalityDataModel.search_mortalities(query)]

                                if result:
                                    if len(result) == 1:
                                        results.append(result[0])
                                continue

        if len(results) == 0:
            return {'message': 'No mortality data matches your search parameters'}, 404

        return {'results': results}, 200


class MortalityDataOne(Resource):
    @requireApiKey
    def get(self):
        query = {}

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
                query['admin_code'] = admin

            subdiv = request.args.get('subdiv', type=str)
            if subdiv:
                if not valid_subdiv(subdiv):
                    return {'message': 'Please enter a valid subdiv code'}, 400
                query['subdiv_code'] = subdiv

            cause = request.args.get('cause', type=str)
            if cause:
                cause_upper = cause.upper()
                if not valid_cause(cause_upper):
                    return {'message': 'Please enter a valid cause code'}, 400
                cause_code_list_extended = {}

                icd_codes = [code.json()
                             for code in IcdModel.find_by_code(cause_upper)]

                for icd_code in icd_codes:
                    matching_codes = [matching_icd_code.json()
                                      for matching_icd_code in IcdModel.search_specific(icd_code['description'])]
                unspecified_codes = []
                generic_codes = []

                pattern = "unspecified"
                match = re.search(pattern, icd_code['description'])
                if not match:
                    unspecified_code = icd_code['description'] + \
                        " (unspecified)"
                    unspecified_codes = [matching_icd_code.json(
                    ) for matching_icd_code in IcdModel.search_specific(unspecified_code)]
                else:

                    position = match.span()
                    start = position[0] - 2
                    end = position[1] + 1

                    generic_code = icd_code['description'][0:start] + \
                        icd_code['description'][end:]
                    generic_codes = [matching_icd_code.json(
                    ) for matching_icd_code in IcdModel.search_specific(generic_code)]

                for matching_code in matching_codes:
                    cause_code_list_extended[matching_code['list']
                                             ] = matching_code['code']

                if generic_codes:
                    for matching_code in generic_codes:
                        cause_code_list_extended[matching_code['list']
                                                 ] = matching_code['code']
                if unspecified_codes:
                    for matching_code in unspecified_codes:
                        cause_code_list_extended[matching_code['list']
                                                 ] = matching_code['code']

                if "103" not in cause_code_list_extended:
                    try:
                        cause_code_list_extended['103'] = cause_code_list_extended['104'][:-1]
                    except:
                        pass

                code_list_entry = CodeListRefModel.find_by_year_and_country(
                    year, country_code)

                try:
                    cause = cause_code_list_extended[code_list_entry.code_list]
                except:
                    return {'message': "Can't find matching cause code for the specified country."}, 400

                query['cause'] = cause

            result = [entry.json()
                      for entry in MortalityDataModel.search_mortalities(query)]

            if code_list_entry.code_list == "104" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(result) == 0:
                cause = cause + "9"
                query['cause'] = cause
                result = [entry.json()
                          for entry in MortalityDataModel.search_mortalities(query)]

            if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(result) == 0:
                cause = cause + "9"
                query['cause'] = cause
                result = [entry.json()
                          for entry in MortalityDataModel.search_mortalities(query)]

            if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 4 and len(result) == 0:
                cause = cause[:-1]
                query['cause'] = cause
                result = [entry.json()
                          for entry in MortalityDataModel.search_mortalities(query)]

            if result:
                if len(result) > 1:
                    return {'message': "More than one mortality entry was found matching your query, please be more specific."}, 400
                return {'entry': result[0]}, 200

            return {'message': "No mortalities match your query."}, 404


class MortalityDataChange(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('admin_code',
                        type=str,
                        )

    parser.add_argument('subdiv_code',
                        type=str,
                        )

    parser.add_argument('code_list',
                        type=str,
                        default="104",
                        )

    parser.add_argument('age_format',
                        type=str,
                        default="00",
                        )

    parser.add_argument('infant_age_format',
                        type=str,
                        default="01",
                        )

    for num in range(1, 27):
        parser.add_argument('deaths' + str(num),
                            type=str,
                            default=""
                            )

    for num in range(1, 5):
        parser.add_argument('infant_deaths' + str(num),
                            type=str,
                            default=""
                            )

    @requireAdmin
    def post(self, country_code, year, sex, cause):

        data = MortalityDataChange.parser.parse_args()

        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        cause_upper = cause.upper()
        if not valid_cause(cause_upper):
            return {'message': 'Please enter a valid cause code'}, 400

        # post_format tells us if we have an admin or subdiv code while allowing us to change their values
        post_format = [0, 0]
        admin_code = data['admin_code']
        if admin_code:
            if not valid_admin(admin_code):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            # delete null value from data object
            del data['admin_code']

        subdiv_code = data['subdiv_code']
        if subdiv_code:
            if not valid_subdiv(subdiv_code):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1
            del data['subdiv_code']

        # if have admin and subdiv
        if post_format[0] and post_format[1]:
            if MortalityDataModel.find_by_casysc(country_code, admin_code, subdiv_code, year, sex, cause):
                return {'message': "An entry already exists for your given year, country, admin, subdiv sex and cause."}, 400

        # if have admin
        if post_format[0] and not post_format[1]:
            if MortalityDataModel.find_by_caysc(country_code, admin_code, year, sex, cause):
                return {'message': "An entry already exists for your given year, country, sex and admin."}, 400
            subdiv_code = ""
            # delete the null values from the data object
            del data['subdiv_code']

        # if have subdiv
        if post_format[1] and not post_format[0]:
            if MortalityDataModel.find_by_csysc(country_code, subdiv_code, year, sex, cause):
                return {'message': "An entry already exists for your given year, country, subdiv, sex and cause."}, 400
            admin_code = ""
            del data['admin_code']

        # if have neither admin or data
        if not post_format[0] and not post_format[1]:
            if MortalityDataModel.find_by_cysc(country_code, year, sex, cause):
                return {'message': "An entry already exists for your given year, country, sex and cause."}, 400
            del data['admin_code']
            admin_code = ""
            del data['subdiv_code']
            subdiv_code = ""

        # code list needs to be a named variable as it comes before cause and sex in the table structure
        code_list = data['code_list']
        del data['code_list']

        entry = MortalityDataModel(country_code, admin_code,
                                   subdiv_code, year, code_list, cause, sex, **data)

        new_code_list_ref = CodeListRefModel(year, country_code, code_list)

        try:
            code_list_ref = CodeListRefModel.find_by_year_and_country(
                year, country_code)
            if code_list_ref.code_list != code_list:
                code_list_ref.code_list = code_list
                code_list_ref.save_to_db()
            else:
                new_code_list_ref.save_to_db()
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the data."}, 500

        return entry.json(), 201

    @requireAdmin
    def put(self, country_code, year, sex, cause):
        data = MortalityDataChange.parser.parse_args()

        # validation
        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        cause_upper = cause.upper()
        if not valid_cause(cause_upper):
            return {'message': 'Please enter a valid cause code'}, 400

        # post_format tells us if we have an admin or subdiv code
        post_format = [0, 0]
        admin_code = data['admin_code']
        if admin_code:
            if not valid_admin(admin_code):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            del data['admin_code']

        subdiv_code = data['subdiv_code']
        if subdiv_code:
            if not valid_subdiv(subdiv_code):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1
            del data['subdiv_code']

        # if have admin and subdiv
        if post_format[0] and post_format[1]:
            entry = MortalityDataModel.find_by_casysc(
                country_code, admin_code, subdiv_code, year, sex, cause)

        # if have admin
        if post_format[0]and not post_format[1]:
            entry = MortalityDataModel.find_by_caysc(
                country_code, admin_code, year, sex, cause)

        # if have subdiv
        if post_format[1] and not post_format[0]:
            entry = MortalityDataModel.find_by_csysc(
                country_code, subdiv_code, year, sex, cause)

        # if have neither admin or data
        if not post_format[0] and not post_format[1]:
            entry = MortalityDataModel.find_by_cysc(
                country_code, year, sex, cause)

        code_list = data['code_list']

        if entry:
            entry.code_list = code_list
            entry.age_format = data['age_format']
            entry.infant_age_format = data['infant_age_format']
            entry.deaths1 = data['deaths1']
            entry.deaths2 = data['deaths2']
            entry.deaths3 = data['deaths3']
            entry.deaths4 = data['deaths4']
            entry.deaths5 = data['deaths5']
            entry.deaths6 = data['deaths6']
            entry.deaths7 = data['deaths7']
            entry.deaths8 = data['deaths8']
            entry.deaths9 = data['deaths9']
            entry.deaths10 = data['deaths10']
            entry.deaths11 = data['deaths11']
            entry.deaths12 = data['deaths12']
            entry.deaths13 = data['deaths13']
            entry.deaths14 = data['deaths14']
            entry.deaths15 = data['deaths15']
            entry.deaths16 = data['deaths16']
            entry.deaths17 = data['deaths17']
            entry.deaths18 = data['deaths18']
            entry.deaths19 = data['deaths19']
            entry.deaths20 = data['deaths20']
            entry.deaths21 = data['deaths21']
            entry.deaths22 = data['deaths22']
            entry.deaths23 = data['deaths23']
            entry.deaths24 = data['deaths24']
            entry.deaths25 = data['deaths25']
            entry.deaths26 = data['deaths26']
            entry.infant_deaths1 = data['infant_deaths1']
            entry.infant_deaths2 = data['infant_deaths2']
            entry.infant_deaths3 = data['infant_deaths3']
            entry.infant_deaths4 = data['infant_deaths4']

        else:
            del data['code_list']
            entry = MortalityDataModel(
                country_code, admin_code, subdiv_code, year, code_list, cause, sex, **data)

        new_code_list_ref = CodeListRefModel(year, country_code, code_list)

        try:
            code_list_ref = CodeListRefModel.find_by_year_and_country(
                year, country_code)
            if code_list_ref.code_list != code_list:
                code_list_ref.code_list = code_list
                code_list_ref.save_to_db()
            else:
                new_code_list_ref.save_to_db()
            entry.save_to_db()
        except:
            return {"message": "An error occurred inserting the data."}, 500

        return entry.json(), 201

    @requireAdmin
    def delete(self, country_code, year, sex, cause):
        data = MortalityDataChange.parser.parse_args()

        if not valid_country_code(country_code):
            return {'message': '{} is not a valid country_code'.format(country_code)}, 400

        if not valid_year(year):
            return {'message': 'Please enter a valid year'}, 400

        if not valid_sex(sex):
            return {'message': 'Please enter a valid sex code'}, 400

        cause_upper = cause.upper()
        if not valid_cause(cause_upper):
            return {'message': 'Please enter a valid cause code'}, 400

        # post_format tells us if we have an admin or subdiv code
        post_format = [0, 0]
        admin_code = data['admin_code']
        if admin_code:
            if not valid_admin(admin_code):
                return {'message': 'Please enter a valid admin code'}, 400
            post_format[0] = 1
            # delete null value from data object

        subdiv_code = data['subdiv_code']
        if subdiv_code:
            if not valid_subdiv(subdiv_code):
                return {'message': 'Please enter a valid subdiv code'}, 400
            post_format[1] = 1

        # if have admin and subdiv
        if post_format[0] and post_format[1]:
            entry = MortalityDataModel.find_by_casysc(
                country_code, admin_code, subdiv_code, year, sex, cause)

        # if have admin
        if post_format[0]and not post_format[1]:
            entry = MortalityDataModel.find_by_caysc(
                country_code, admin_code, year, sex, cause)

        # if have subdiv
        if post_format[1] and not post_format[0]:
            entry = MortalityDataModel.find_by_csysc(
                country_code, subdiv_code, year, sex, cause)

        # if have neither admin or data
        if not post_format[0] and not post_format[1]:
            entry = MortalityDataModel.find_by_cysc(
                country_code, year, sex, cause)

        if entry:
            if len(entry) > 1:
                return {'message': "More than one mortality entry was found with the given parameters. Please supply either an admin or subdiv code as required.",
                        'entries': [mortality.json() for mortality in entry]}, 400
            entry[0].delete_from_db()
            return {'message': 'Entry deleted.'}
        return {'message': 'Item not found.'}, 404
