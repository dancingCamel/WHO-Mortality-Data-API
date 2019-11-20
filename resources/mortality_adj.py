from flask_restful import Resource, request
from models.mortality import MortalityDataModel
from models.population import PopulationModel
from models.country import CountryModel
from validate import *
import math


class MortalityAdjustedSearch(Resource):
    def get(self):
        # find all results for mortality search then change values depending on population per 100,000. round?

        # use get_args() for variables. search with dict. Two dicts, one for mortality, one for population
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

        subdiv = request.args.get('subdiv', type=str)
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400

        cause = request.args.get('cause', type=str)
        # add validation fo cause
        if cause:
            query['cause'] = cause

        # results of mortality search in list
        results = [entry.json()
                   for entry in MortalityDataModel.search_mortalities(query)]

        if not results:
            return {'message': "No mortality entries match your query."}, 404

        # for each item in the results lits, find the corresponding population
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

                    # always round data up
                    def round_up(n, decimals=100):
                        multiplier = 10 ** decimals
                        return math.ceil(n * multiplier) / multiplier

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
                                    round_up(int(value)/int(pop)*100000, 3))
                            if pop == None:
                                ages_to_delete.append(age_range)
                        for index in ages_to_delete:
                            del entry[key][index]
                    else:
                        entry[key] = str(
                            round_up(int(value)/int(pop_data[key])*100000, 3))

            return {'adjusted_entries': results}, 200


class MortalityAdjustedOne(Resource):
    def get(self):
        # find all results for mortality search then change values depending on population per 100,000. round?

        # use get_args() for variables. search with dict. Two dicts, one for mortality, one for population
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

        subdiv = request.args.get('subdiv', type=str)
        if subdiv:
            if not valid_subdiv(subdiv):
                return {'message': 'Please enter a valid subdiv code'}, 400

        cause = request.args.get('cause', type=str)
        # add validation fo cause
        if cause:
            query['cause'] = cause

        # results of mortality search in list
        results = [entry.json()
                   for entry in MortalityDataModel.search_mortalities(query)]

        if not results:
            return {'message': "No mortality entries match your query."}, 404

        if results:
            if len(results) > 1:
                return {'message': "More than one population entry was found matching your query."}, 400

            # for each item in the results lits, find the corresponding population
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

                    # always round data up
                    def round_up(n, decimals=100):
                        multiplier = 10 ** decimals
                        return math.ceil(n * multiplier) / multiplier

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
                                    round_up(int(value)/int(pop)*100000, 3))
                            if pop == None:
                                ages_to_delete.append(age_range)
                        for index in ages_to_delete:
                            del entry[key][index]
                    else:
                        entry[key] = str(
                            round_up(int(value)/int(pop_data[key])*100000, 3))

            return {'adjusted_entries': results}, 200
