import re
import math
from flask_restful import Resource, request
from auth import requireApiKey
from models.mortality import MortalityDataModel
from models.population import PopulationModel
from models.country import CountryModel
from models.icd import IcdModel
from models.code_list_ref import CodeListRefModel
from validate import *


def round_up(n, decimals=100):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


class MortalityAdjustedSearch(Resource):
    @requireApiKey
    def get(self):
        # find all results for mortality search then change values depending on population per 100,000.

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

            # add to extended code list
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

        if not results:
            return {'message': "No mortality entries match your query."}, 404

        # for each item in the results list find the corresponding population
        for entry in results:
            pop_query = {}
            pop_query['country_code'] = entry['country']['code']
            pop_query['year'] = entry['year']
            pop_query['sex'] = entry['sex']['code']

            admin = entry['admin']
            if admin != "None":
                pop_query['admin'] = admin['code']

            subdiv = entry['subdiv']
            if subdiv != "None":
                pop_query['subdiv'] = subdiv['code']

            pop_data = PopulationModel.search_single_population(
                pop_query)
            if pop_data:
                pop_data = pop_data.json()
            else:
                country = CountryModel.find_by_code(
                    country_code).json()
                return {'message': "No population data available for '{}' in year {} for sex '{}'.".format(country['description'], year, sex)}, 404

            # remove infant mortality data as no related population data given
            del entry['infant_age_breakdown']
            # delete age format numbers as now irrelevant
            del entry['age_format']
            del entry['infant_age_format']

            # divide mortality data by corresponding population number and multiply by 100,000
            # population is population of that specific age/sex. not total country population
            things_to_skip = ["country", "admin", "subdiv", "year",
                              "code_list", "cause", "sex", "infant_age_breakdown"]
            for key, value in entry.items():
                if key in things_to_skip:
                    continue

                # format age_breakdown data per 100,000
                if key == "age_breakdown":
                    ages_to_delete = []
                    for age_range, value in entry[key].items():
                        pop = pop_data[key].get(age_range)
                        entry[key][age_range] = pop
                        if pop:
                            if pop == "0":
                                continue
                            entry[key][age_range] = str(
                                round_up(float(value)/float(pop)*100000, 3))
                        if pop == None:
                            ages_to_delete.append(age_range)
                    for index in ages_to_delete:
                        del entry[key][index]
                else:
                    entry[key] = str(
                        round_up(float(value)/float(pop_data[key])*100000, 3))

        return {'adjusted_entries': results}, 200


class MortalityAdjustedSearchMultiple(Resource):
    @requireApiKey
    def get(self):

        def strip_whitespace(string):
            return ('').join(string.split(' '))

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

        # results of each mortality adj search
        results = []
        # loop over all permutations of list items and validate codes.
        for country_code in filter(valid_country_code, country_code_list):
            for year in filter(valid_year, year_list):
                for sex in filter(valid_sex, sex_code_list):
                    for cause in filter(valid_cause, cause_code_list):
                        for admin in filter(valid_admin, admin_code_list):
                            for subdiv in filter(valid_subdiv, subdiv_code_list):

                                # generate query
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
                                    if len(result) > 1:
                                        continue

                                # adjust for population and add to results list
                                for entry in result:
                                    pop_query = {}
                                    pop_query['country_code'] = entry['country']['code']
                                    pop_query['year'] = entry['year']
                                    pop_query['sex'] = entry['sex']['code']

                                    admin = entry['admin']
                                    if admin != "None":
                                        pop_query['admin'] = admin['code']

                                    subdiv = entry['subdiv']
                                    if subdiv != "None":
                                        pop_query['subdiv'] = subdiv['code']

                                    pop_data = PopulationModel.search_single_population(
                                        pop_query)
                                    if pop_data:
                                        pop_data = pop_data.json()
                                    else:
                                        country = CountryModel.find_by_code(
                                            country_code).json()

                                        del entry['infant_age_breakdown']
                                        del entry['age_format']
                                        del entry['infant_age_format']
                                        del entry['age_breakdown']
                                        entry['all_ages'] = "No population data."
                                        continue

                                    # remove infant mortality data as no related population data given
                                    del entry['infant_age_breakdown']
                                    # delete age format numbers as now irrelevant
                                    del entry['age_format']
                                    del entry['infant_age_format']

                                    # divide mortality data by corresponding population number and multiply by 100,000
                                    # population is population of that specific age/sex. not total country population
                                    things_to_skip = ["country", "admin", "subdiv", "year",
                                                      "code_list", "cause", "sex", "infant_age_breakdown"]
                                    for key, value in entry.items():
                                        if key in things_to_skip:
                                            continue

                                        # format age_breakdown data per 100,000
                                        if key == "age_breakdown":
                                            ages_to_delete = []
                                            for age_range, value in entry[key].items():
                                                pop = pop_data[key].get(
                                                    age_range)
                                                entry[key][age_range] = pop
                                                if pop:
                                                    if pop == "0":
                                                        continue
                                                    entry[key][age_range] = str(
                                                        round_up(float(value)/float(pop)*100000, 3))
                                                if pop == None:
                                                    ages_to_delete.append(
                                                        age_range)
                                            for index in ages_to_delete:
                                                del entry[key][index]
                                        else:
                                            entry[key] = str(
                                                round_up(float(value)/float(pop_data[key])*100000, 3))

                                # append to results list if anything found
                                if result:
                                    results.append(result[0])

        if len(results) == 0:
            return {'message': "No mortality entries match your query."}, 404

        return {'results': results}, 200


class MortalityAdjustedOne(Resource):
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

        results = [entry.json()
                   for entry in MortalityDataModel.search_mortalities(query)]

        if code_list_entry.code_list == "104" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(results) == 0:
            cause = cause + "9"
            query['cause'] = cause
            results = [entry.json()
                       for entry in MortalityDataModel.search_mortalities(query)]

        if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 3 and len(results) == 0:
            cause = cause + "9"
            query['cause'] = cause
            result = [entry.json()
                      for entry in MortalityDataModel.search_mortalities(query)]

        if code_list_entry.code_list == "10M" and len(cause_code_list_extended[code_list_entry.code_list]) == 4 and len(results) == 0:
            cause = cause[:-1]
            query['cause'] = cause
            result = [entry.json()
                      for entry in MortalityDataModel.search_mortalities(query)]

        if not results:
            return {'message': "No mortality entries match your query."}, 404

        if results:
            if len(results) > 1:
                return {'message': "More than one population entry was found matching your query."}, 400

            for entry in results:
                pop_query = {}
                pop_query['country_code'] = entry['country']['code']
                pop_query['year'] = entry['year']
                pop_query['sex'] = entry['sex']['code']

                admin = entry['admin']
                if admin != "None":
                    pop_query['admin'] = admin['code']

                subdiv = entry['subdiv']
                if subdiv != "None":
                    pop_query['subdiv'] = subdiv['code']
                pop_data = PopulationModel.search_single_population(
                    pop_query)
                if pop_data:
                    pop_data = pop_data.json()
                else:
                    country = CountryModel.find_by_code(
                        country_code).json()
                    return {'message': "No population data available for '{}' in year {} for sex '{}'.".format(country['description'], year, sex)}, 404

                del entry['infant_age_breakdown']
                del entry['age_format']
                del entry['infant_age_format']

                things_to_skip = ["country", "admin", "subdiv", "year",
                                  "code_list", "cause", "sex", "infant_age_breakdown"]
                for key, value in entry.items():
                    if key in things_to_skip:
                        continue

                    # format age_breakdown data per 100,000
                    if key == "age_breakdown":
                        ages_to_delete = []
                        for age_range, value in entry[key].items():
                            pop = pop_data[key].get(age_range)
                            entry[key][age_range] = pop
                            if pop:
                                if pop == "0":
                                    continue
                                entry[key][age_range] = str(
                                    round_up(float(value)/float(pop)*100000, 3))
                            if pop == None:
                                ages_to_delete.append(age_range)
                        for index in ages_to_delete:
                            del entry[key][index]
                    else:
                        entry[key] = str(
                            round_up(float(value) /
                                     float(pop_data[key])*100000, 3))

            return {'adjusted_entries': results}, 200
