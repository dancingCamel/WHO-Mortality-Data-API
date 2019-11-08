import csv
from models.country import CountryModel
from models.population import PopulationModel


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

            # can't check if in table as don't have unique identifiers
            new_population_object.save_to_db()
