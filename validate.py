from models.sex import SexModel
from models.country import CountryModel
from models.admin import AdminModel
from models.subdiv import SubdivModel
from models.icd10 import Icd10Model
from datetime import datetime


def valid_year(year):
    first_year = 1950
    this_year = datetime.now().year
    try:
        int(year)
        if int(year) in range(first_year, this_year):
            return True
        return False
    except:
        return False


def valid_sex(sex):
    valid_codes = ['1', '2', '9']
    if sex in valid_codes:
        return True
    return False


def valid_country_code(country_code):
    if CountryModel.find_by_code(country_code):
        return True
    return False


def valid_admin(admin):
    if AdminModel.find_by_code(admin) or admin == "":
        return True
    return False


def valid_subdiv(subdiv):
    if SubdivModel.find_by_code(subdiv) or subdiv == "":
        return True
    return False


def valid_cause(cause):
    cause = cause.upper()
    if Icd10Model.find_by_code(cause):
        return True
    return False
