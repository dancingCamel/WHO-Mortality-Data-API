from models.sex import SexModel
from models.country import CountryModel
from datetime import datetime


def validate_year(year):
    first_year = 1988
    this_year = datetime.now().year
    try:
        int(year)
        if int(year) not in range(first_year, this_year):
            return {'message': 'Please enter a year in range {0} - {1}'.format(first_year, this_year)}, 400
        str(year)
    except:
        return {'message': 'Please enter a year in range {0} - {1}'.format(first_year, this_year)}, 400


def validate_sex(sex):
    try:
        int(sex)
        str(sex)
        sex = SexModel.find_by_code(sex).sex_code
    except:
        sex = SexModel.find_by_name(sex)
        if sex:
            sex = sex.sex_code
        if not sex:
            return {'message': 'Please enter a valid sex code'}, 400


def validate_country_code(country_code):
    if not CountryModel.find_by_code(country_code):
        return {'message': '{} is not a valid country_code'.format(country_code)}, 400
