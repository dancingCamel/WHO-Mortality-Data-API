import csv
from models.country import CountryModel


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
