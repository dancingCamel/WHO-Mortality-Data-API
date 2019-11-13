import csv
from models.country import CountryModel
from models.population import PopulationModel
from models.sex import SexModel
from models.admin import AdminModel
from models.subdiv import SubdivModel
from models.age_format import AgeFormatModel
from models.infant_age_format import InfantAgeFormatModel
from codes import *


def populate_country_table():
    # open each line of csv file
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
