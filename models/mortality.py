from db import db
from models.country import CountryModel
from models.admin import AdminModel
from models.subdiv import SubdivModel
from models.icd import IcdModel
from models.sex import SexModel
from models.age_format import AgeFormatModel
from models.infant_age_format import InfantAgeFormatModel


class MortalityDataModel(db.Model):
    __tablename__ = 'mortality_data'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(5))
    admin_code = db.Column(db.String(5))
    subdiv_code = db.Column(db.String(5))
    year = db.Column(db.String(5))
    code_list = db.Column(db.String(5))
    cause = db.Column(db.String(5))
    sex = db.Column(db.String(5))
    age_format = db.Column(db.String(5))
    infant_age_format = db.Column(db.String(5))
    deaths1 = db.Column(db.String(15))
    deaths2 = db.Column(db.String(15))
    deaths3 = db.Column(db.String(15))
    deaths4 = db.Column(db.String(15))
    deaths5 = db.Column(db.String(15))
    deaths6 = db.Column(db.String(15))
    deaths7 = db.Column(db.String(15))
    deaths8 = db.Column(db.String(15))
    deaths9 = db.Column(db.String(15))
    deaths10 = db.Column(db.String(15))
    deaths11 = db.Column(db.String(15))
    deaths12 = db.Column(db.String(15))
    deaths13 = db.Column(db.String(15))
    deaths14 = db.Column(db.String(15))
    deaths15 = db.Column(db.String(15))
    deaths16 = db.Column(db.String(15))
    deaths17 = db.Column(db.String(15))
    deaths18 = db.Column(db.String(15))
    deaths19 = db.Column(db.String(15))
    deaths20 = db.Column(db.String(15))
    deaths21 = db.Column(db.String(15))
    deaths22 = db.Column(db.String(15))
    deaths23 = db.Column(db.String(15))
    deaths24 = db.Column(db.String(15))
    deaths25 = db.Column(db.String(15))
    deaths26 = db.Column(db.String(15))
    infant_deaths1 = db.Column(db.String(15))
    infant_deaths2 = db.Column(db.String(15))
    infant_deaths3 = db.Column(db.String(15))
    infant_deaths4 = db.Column(db.String(15))

    def __init__(self, country_code, admin_code, subdiv_code, year, code_list, cause, sex, age_format, infant_age_format, deaths1, deaths2, deaths3, deaths4, deaths5, deaths6, deaths7, deaths8, deaths9, deaths10, deaths11, deaths12, deaths13, deaths14, deaths15, deaths16, deaths17, deaths18, deaths19, deaths20, deaths21, deaths22, deaths23, deaths24, deaths25, deaths26, infant_deaths1, infant_deaths2, infant_deaths3, infant_deaths4):
        self.country_code = country_code
        self.admin_code = admin_code
        self.subdiv_code = subdiv_code
        self.year = year
        self.code_list = code_list
        self.cause = cause
        self.sex = sex
        self.age_format = age_format
        self.infant_age_format = infant_age_format
        self.deaths1 = deaths1
        self.deaths2 = deaths2
        self.deaths3 = deaths3
        self.deaths4 = deaths4
        self.deaths5 = deaths5
        self.deaths6 = deaths6
        self.deaths7 = deaths7
        self.deaths8 = deaths8
        self.deaths9 = deaths9
        self.deaths10 = deaths10
        self.deaths11 = deaths11
        self.deaths12 = deaths12
        self.deaths13 = deaths13
        self.deaths14 = deaths14
        self.deaths15 = deaths15
        self.deaths16 = deaths16
        self.deaths17 = deaths17
        self.deaths18 = deaths18
        self.deaths19 = deaths19
        self.deaths20 = deaths20
        self.deaths21 = deaths21
        self.deaths22 = deaths22
        self.deaths23 = deaths23
        self.deaths24 = deaths24
        self.deaths25 = deaths25
        self.deaths26 = deaths26
        self.infant_deaths1 = infant_deaths1
        self.infant_deaths2 = infant_deaths2
        self.infant_deaths3 = infant_deaths3
        self.infant_deaths4 = infant_deaths4

    def json(self):
        # format country
        country = CountryModel.find_by_code(self.country_code)
        if country:
            country = {'code': self.country_code,
                       'description': country.country_name}
        else:
            country = "Country with code {} not found.".format(
                self.country_code), 404

        # format admin
        admin = AdminModel.find_by_code_and_country(
            self.admin_code, self.country_code)
        if admin:
            admin = {'code': admin.admin_code,
                     'description': admin.description}
        else:
            admin = 'None'

        # format subdiv
        subdiv = SubdivModel.find_by_code(self.subdiv_code)
        if subdiv:
            subdiv = {'code': subdiv.subdiv_code,
                      'description': subdiv.description}
        else:
            subdiv = 'None'

        # format cause
        cause = IcdModel.find_by_list_and_code(self.code_list, self.cause)
        if cause:
            cause = {'code': cause.code,
                     'description': cause.description}
        else:
            cause = "Cause code '{}' not found in list '{}'".format(
                self.cause, self.code_list), 404

        # format sex
        sex = SexModel.find_by_code(self.sex)
        if sex:
            sex = sex.json()
        else:
            sex = "Sex with code {} not found.".format(self.sex)

        # format age to remove blanks
        age_breakdown_format = AgeFormatModel.find_by_code(
            self.age_format)

        if age_breakdown_format:
            age_breakdown_format = age_breakdown_format.json()
        else:
            return {'message': "No age breakdown found for code '{}'.".format(self.age_format)}, 404

        deaths = [
            self.deaths2,
            self.deaths3,
            self.deaths4,
            self.deaths5,
            self.deaths6,
            self.deaths7,
            self.deaths8,
            self.deaths9,
            self.deaths10,
            self.deaths11,
            self.deaths12,
            self.deaths13,
            self.deaths14,
            self.deaths15,
            self.deaths16,
            self.deaths17,
            self.deaths18,
            self.deaths19,
            self.deaths20,
            self.deaths21,
            self.deaths22,
            self.deaths23,
            self.deaths24,
            self.deaths25,
            self.deaths26
        ]
        age_breakdown = {}
        count = 0
        for death, age_range in age_breakdown_format.items():
            if death == "age_format_code":
                continue
            age_breakdown[age_range] = deaths[count]
            count += 1
        empties = []
        for age_range, value in age_breakdown.items():
            if value == "":
                empties.append(age_range)
        for index in empties:
            del age_breakdown[index]

        # format infant age to remove blanks
        infant_age_breakdown_format = InfantAgeFormatModel.find_by_code(
            self.infant_age_format)

        if infant_age_breakdown_format:
            infant_age_breakdown_format = infant_age_breakdown_format.json()
        else:
            return {'message': "No infant age breakdown found for code '{}'.".format(self.infant_age_format)}, 404

        infant_deaths = [
            self.infant_deaths1,
            self.infant_deaths2,
            self.infant_deaths3,
            self.infant_deaths4
        ]
        infant_age_breakdown = {}
        count = 0
        for infant_death, age_range in infant_age_breakdown_format.items():
            if infant_death == "infant_age_format_code":
                continue
            infant_age_breakdown[age_range] = infant_deaths[count]
            count += 1
        empties = []
        for infant_age_range, value in infant_age_breakdown.items():
            if value == "":
                empties.append(infant_age_range)
        for index in empties:
            del infant_age_breakdown[index]

        return {
            'country': country,
            'admin': admin,
            'subdiv': subdiv,
            'year': self.year,
            'code_list': self.code_list,
            'cause': cause,
            'sex': sex,
            'age_format': self.age_format,
            'infant_age_format': self.infant_age_format,
            'all_ages': self.deaths1,
            'age_breakdown': age_breakdown,
            'infant_age_breakdown': infant_age_breakdown,
        }

    def json_unformatted(self):
        return {
            'country_code': self.country_code,
            'admin_code': self.admin_code,
            'subdiv_code': self.subdiv_code,
            'year': self.year,
            'code_list': self.code_list,
            'cause': self.cause,
            'sex': self.sex,
            'age_format': self.age_format,
            'infant_age_format': self.infant_age_format,
            'deaths1': self.deaths1,
            'deaths2': self.deaths2,
            'deaths3': self.deaths3,
            'deaths4': self.deaths4,
            'deaths5': self.deaths5,
            'deaths6': self.deaths6,
            'deaths7': self.deaths7,
            'deaths8': self.deaths8,
            'deaths9': self.deaths9,
            'deaths10': self.deaths10,
            'deaths11': self.deaths11,
            'deaths12': self.deaths12,
            'deaths13': self.deaths13,
            'deaths14': self.deaths14,
            'deaths15': self.deaths15,
            'deaths16': self.deaths16,
            'deaths17': self.deaths17,
            'deaths18': self.deaths18,
            'deaths19': self.deaths19,
            'deaths20': self.deaths20,
            'deaths21': self.deaths21,
            'deaths22': self.deaths22,
            'deaths23': self.deaths23,
            'deaths24': self.deaths24,
            'deaths25': self.deaths25,
            'deaths26': self.deaths26,
            'infant_deaths1': self.infant_deaths1,
            'infant_deaths2': self.infant_deaths2,
            'infant_deaths3': self.infant_deaths3,
            'infant_deaths4': self.infant_deaths4
        }

    # class methods:
    # don't need to search with list as each country will only use one list in a given year
    @classmethod
    def search_mortalities(cls, kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def search_single_mortality(cls, kwargs):
        # search_single - validate the dictionary to ensure it contains enough info to select just one entry.
        # must include country, year, sex, cause, admin, subdiv
        return cls.query.filter_by(**kwargs).first()

    # /country/year/sex/cause endpoint and use parser to get admin and subdiv codes
    # put and post functions
    @classmethod
    def find_by_caysc(cls, country_code, admin_code, year, sex, cause):
        return cls.query.filter_by(country_code=country_code, admin_code=admin_code, year=year, sex=sex, cause=cause).all()

    @classmethod
    def find_by_csysc(cls, country_code, subdiv_code, year, sex, cause):
        return cls.query.filter_by(country_code=country_code, subdiv_code=subdiv_code, year=year, sex=sex, cause=cause).all()

    @classmethod
    def find_by_cysc(cls, country_code, year, sex, cause):
        return cls.query.filter_by(country_code=country_code, year=year, sex=sex, cause=cause).all()

    # use in the delete function
    @classmethod
    def find_by_casysc(cls, country_code, admin_code, subdiv_code, year, sex, cause):
        return cls.query.filter_by(country_code=country_code, admin_code=admin_code, subdiv_code=subdiv_code, year=year, sex=sex, cause=cause).all()

    # use in populate_code_list_reference
    @classmethod
    def find_all_years(cls):

        query = cls.query.with_entities(cls.year).distinct().all()
        years = [int(row.year) for row in query]
        return years

    @classmethod
    def find_by_cy(cls, country_code, year):
        return cls.query.filter_by(country_code=country_code, year=year).first()

    @classmethod
    def find_by_year(cls, year):
        return cls.query.filter_by(year=year).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
