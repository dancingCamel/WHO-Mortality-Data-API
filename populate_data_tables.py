import csv
import json
from models.country import CountryModel
from models.population import PopulationModel
from models.sex import SexModel
from models.admin import AdminModel
from models.subdiv import SubdivModel
from models.age_format import AgeFormatModel
from models.infant_age_format import InfantAgeFormatModel
from models.icd import IcdModel
from models.icd_lists import IcdListsModel
from models.mortality import MortalityDataModel
from models.superuser import SuperuserModel
from models.code_list_ref import CodeListRefModel
from codes import *

# use break instead of continue - if it finds an entry the table exists. Skip populating that table
# assume our data sets have no duplicates


def populate_code_list_reference():
    data = {}

    year_list = MortalityDataModel.find_all_years()
    min_year = min(year_list)
    max_year = max(year_list)

    # make dictionary so don't get duplicate entries
    for year in range(min_year, max_year):
        year_data = MortalityDataModel.find_by_year(str(year))

        individual_year_object = {}
        for row in year_data:
            if row.country_code in individual_year_object:
                continue
            individual_year_object[row.country_code] = row.code_list

        data[str(year)] = individual_year_object

    # extract each item in dictionary and save it to db
    for year, year_data in data.items():
        for country_code, code_list in year_data.items():
            entry = CodeListRefModel(
                year=str(year), country_code=country_code, code_list=code_list)
            entry.save_to_db()


def populate_code_list_reference():
    # alternate function that uses less memory - doesn't work
    year_list = MortalityDataModel.find_all_years()
    min_year = min(year_list)
    max_year = max(year_list)

    countries = [country.json() for country in CountryModel.find_all()]

    for year in range(min_year, max_year):
        individual_year_object = {}
        for country in countries:
            country_code = country['code']

            code_list_ref_entry = CodeListRefModel.find_by_year_and_country(
                year=str(year), country_code=country_code)
            if code_list_ref_entry:
                continue

            # this takes way too long - leads to timeout
            mortality_entry = MortalityDataModel.find_by_cy(
                country_code=country_code, year=str(year))

            if mortality_entry:
                new_entry = CodeListRefModel(
                    year=str(year), country_code=country_code, code_list=mortality_entry.code_list)
                new_entry.save_to_db()
            continue

# alternative version using csv file


def populate_country_table():
    # with open('/var/www/html/items-rest/raw_data/code_list_ref.csv', 'r') as code_file:
    with open('./raw_data/code_list_ref.csv', 'r') as code_file:
        code_list_ref_reader = csv.reader(code_file)
        for row in code_list_ref_reader:
            new_entry = CodeListRefModel(*row)

            entry = CodeListRefModel.find_by_year_and_country(
                new_entry.year, new_entry.country_code)
            if entry:
                continue
            else:
                if new_entry.country_code == "country_code":
                    continue
                new_entry.save_to_db()


def populate_country_table():
    # when working locally use ./raw_data for relative file path.
    # when running on remote server use abolute file path
    # with open('/var/www/html/items-rest/raw_data/country_codes.csv', 'r') as country_code_file:
    with open('./raw_data/country_codes.csv', 'r') as country_code_file:
        country_reader = csv.reader(country_code_file)
        for row in country_reader:
            # make it a CountryModel object
            new_country_object = CountryModel(*row)

            # check if it's in the table
            country = CountryModel.find_by_code(
                new_country_object.country_code)
            if country:
                continue
            else:
                if new_country_object.country_name == "name":
                    continue
                new_country_object.save_to_db()


def populate_population_table():
    # with open('/var/www/html/items-rest/raw_data/populations.csv', 'r') as population_file:
    with open('./raw_data/populations.csv', 'r') as population_file:

        pop_reader = csv.reader(population_file)
        for row in pop_reader:

            # make it a PopulationModel object
            new_population_object = PopulationModel(*row)

            if new_population_object.year == "Year":
                continue

            population = PopulationModel.find_by_cysas(new_population_object.country_code, new_population_object.year,
                                                       new_population_object.sex, new_population_object.admin, new_population_object.subdiv)
            if population:
                continue

            # can't check if in table as don't have unique identifiers
            new_population_object.save_to_db()


def populate_sex_table():
    for sex, sex_code in sex_codes.items():
        if SexModel.find_by_name(sex):
            continue
        new_sex_object = SexModel(sex, sex_code)
        new_sex_object.save_to_db()


def populate_admin_table():
    for row in admin_codes:
        new_admin_model = AdminModel(*row)
        if AdminModel.find_by_code_and_country(new_admin_model.admin_code, new_admin_model.country_code):
            continue
        new_admin_model.save_to_db()


def populate_subdiv_table():
    for subdiv_code, description in subdiv_codes.items():
        if SubdivModel.find_by_code(subdiv_code):
            continue
        new_subdiv_object = SubdivModel(subdiv_code, description)
        new_subdiv_object.save_to_db()


def populate_age_format_table():
    for age_format_code, format_list in age_format_codes.items():
        if AgeFormatModel.find_by_code(age_format_code):
            continue

        new_age_format = AgeFormatModel(age_format_code, *format_list)
        new_age_format.save_to_db()


def populate_infant_age_format_table():
    for infant_age_format_code, format_list in infant_age_format_codes.items():
        if InfantAgeFormatModel.find_by_code(infant_age_format_code):
            continue

        new_infant_age_format = InfantAgeFormatModel(
            infant_age_format_code, *format_list)
        new_infant_age_format.save_to_db()


def populate_icd_table_101():
    # with open('/var/www/html/items-rest/raw_data/icd10-code-lists/101.csv', 'r') as code_file:
    with open('./raw_data/icd10-code-lists/101.csv', 'r') as code_file:

        code_reader = csv.reader(code_file)
        for row in code_reader:
            code_list = '101'
            new_icd_object = IcdModel(code_list, *row)

            entry = IcdModel.find_by_list_and_code(
                new_icd_object.code_list, new_icd_object.code)
            if entry:
                continue

            new_icd_object.save_to_db()


def populate_icd_table_103():
    # with open('/var/www/html/items-rest/raw_data/icd10-code-lists/103.csv', 'r') as code_file:
    with open('./raw_data/icd10-code-lists/103.csv', 'r') as code_file:
        code_reader = csv.reader(code_file)
        for row in code_reader:
            code_list = '103'
            new_icd_object = IcdModel(code_list, *row)

            entry = IcdModel.find_by_list_and_code(
                new_icd_object.code_list, new_icd_object.code)
            if entry:
                continue

            new_icd_object.save_to_db()


def populate_icd_table_104():
    # with open('/var/www/html/items-rest/raw_data/icd10-code-lists/104.csv', 'r') as code_file:
    with open('./raw_data/icd10-code-lists/104.csv', 'r') as code_file:
        code_reader = csv.reader(code_file)
        for row in code_reader:
            code_list = '104'
            new_icd_object = IcdModel(code_list, *row)

            entry = IcdModel.find_by_list_and_code(
                new_icd_object.code_list, new_icd_object.code)
            if entry:
                continue

            new_icd_object.save_to_db()


def populate_icd_table_10M():
    # with open('/var/www/html/items-rest/raw_data/icd10-code-lists/10M.csv', 'r') as code_file:
    with open('./raw_data/icd10-code-lists/10M.csv', 'r') as code_file:

        code_reader = csv.reader(code_file)
        for row in code_reader:
            code_list = "10M"
            new_icd_object = IcdModel(code_list, *row)

            entry = IcdModel.find_by_list_and_code(
                new_icd_object.code_list, new_icd_object.code)
            if entry:
                continue

            new_icd_object.save_to_db()


def populate_icd_table_UE1():
    # with open('/var/www/html/items-rest/raw_data/icd10-code-lists/UE1.csv', 'r') as code_file:
    with open('./raw_data/icd10-code-lists/UE1.csv', 'r') as code_file:
        code_reader = csv.reader(code_file)
        for row in code_reader:
            code_list = "UE1"
            new_icd_object = IcdModel(code_list, *row)

            entry = IcdModel.find_by_list_and_code(
                new_icd_object.code_list, new_icd_object.code)
            if entry:
                continue

            new_icd_object.save_to_db()


def populate_icd_code_lists_table():
    for code, description in icd_lists.items():
        if IcdListsModel.find_by_code(code):
            continue

        new_list = IcdListsModel(code, description)
        new_list.save_to_db()


def populate_mortality_table():
    # with open('/var/www/html/items-rest/raw_data/Mort-ICD10.csv', 'r') as mort_file:
    with open('./raw_data/Mort-ICD10.csv', 'r') as mort_file:
        mort_reader = csv.reader(mort_file)
        for row in mort_reader:
            new_mortality_entry = MortalityDataModel(*row)
            # too much data to check each line each time

            new_mortality_entry.save_to_db()
            # this takes way too long. need to find another way of generating the table more quickly
            # this way would take over 15 hours


def add_total_population_entries():
    pass
    # need array of all possible years, all possible sexes and all possible admins and subdivs and all possible countires
    # loop through each array nested. check to see if exists and save them to vars
    # return the json_unformated. add relevant numbers together and save new entry to db


def add_first_admin():
    username = "whomortalitydatabase@gmail.com"

    superuser = SuperuserModel(username)
    superuser.save_to_db()
