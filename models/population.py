from db import db
from models.country import CountryModel
from models.sex import SexModel


class PopulationModel(db.Model):
    __tablename__ = "populations"

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(5))
    admin = db.Column(db.String(5))
    subdiv = db.Column(db.String(5))
    year = db.Column(db.String(5))
    sex = db.Column(db.String(5))
    age_format = db.Column(db.String(5))
    pop1 = db.Column(db.String(15))
    pop2 = db.Column(db.String(15))
    pop3 = db.Column(db.String(15))
    pop4 = db.Column(db.String(15))
    pop5 = db.Column(db.String(15))
    pop6 = db.Column(db.String(15))
    pop7 = db.Column(db.String(15))
    pop8 = db.Column(db.String(15))
    pop9 = db.Column(db.String(15))
    pop10 = db.Column(db.String(15))
    pop11 = db.Column(db.String(15))
    pop12 = db.Column(db.String(15))
    pop13 = db.Column(db.String(15))
    pop14 = db.Column(db.String(15))
    pop15 = db.Column(db.String(15))
    pop16 = db.Column(db.String(15))
    pop17 = db.Column(db.String(15))
    pop18 = db.Column(db.String(15))
    pop19 = db.Column(db.String(15))
    pop20 = db.Column(db.String(15))
    pop21 = db.Column(db.String(15))
    pop22 = db.Column(db.String(15))
    pop23 = db.Column(db.String(15))
    pop24 = db.Column(db.String(15))
    pop25 = db.Column(db.String(15))
    pop26 = db.Column(db.String(15))
    live_births = db.Column(db.String(15))

    def __init__(self, country_code, admin, subdiv, year, sex, age_format, pop1, pop2, pop3, pop4, pop5, pop6, pop7, pop8, pop9, pop10, pop11, pop12, pop13, pop14, pop15, pop16, pop17, pop18, pop19, pop20, pop21, pop22, pop23, pop24, pop25, pop26, live_births):
        self.country_code = country_code
        self.admin = admin
        self.subdiv = subdiv
        self.year = year
        self.sex = sex
        self.age_format = age_format
        self.pop1 = pop1
        self.pop2 = pop2
        self.pop3 = pop3
        self.pop4 = pop4
        self.pop5 = pop5
        self.pop6 = pop6
        self.pop7 = pop7
        self.pop8 = pop8
        self.pop9 = pop9
        self.pop10 = pop10
        self.pop11 = pop11
        self.pop12 = pop12
        self.pop13 = pop13
        self.pop14 = pop14
        self.pop15 = pop15
        self.pop16 = pop16
        self.pop17 = pop17
        self.pop18 = pop18
        self.pop19 = pop19
        self.pop20 = pop20
        self.pop21 = pop21
        self.pop22 = pop22
        self.pop23 = pop23
        self.pop24 = pop24
        self.pop25 = pop25
        self.pop26 = pop26
        self.live_births = live_births

    def json(self):
        return {
            'id': self.id,
            # 'country_code': self.country_code,
            'country': CountryModel.find_by_code(self.country_code).json(),
            'admin': self.admin,
            'subdiv': self.subdiv,
            'year': self.year,
            'sex': SexModel.find_by_code(self.sex),
            'age_format': self.age_format,
            'population_all_ages': int(self.pop1),
            # remove blanks with formating then change all to ints
            'pop2': self.pop2,
            'pop3': self.pop3,
            'pop4': self.pop4,
            'pop5': self.pop5,
            'pop6': self.pop6,
            'pop7': self.pop7,
            'pop8': self.pop8,
            'pop9': self.pop9,
            'pop10': self.pop10,
            'pop11': self.pop11,
            'pop12': self.pop12,
            'pop13': self.pop13,
            'pop14': self.pop14,
            'pop15': self.pop15,
            'pop16': self.pop16,
            'pop17': self.pop17,
            'pop18': self.pop18,
            'pop19': self.pop19,
            'pop20': self.pop20,
            'pop21': self.pop21,
            'pop22': self.pop22,
            'pop23': self.pop23,
            'pop24': self.pop24,
            'pop25': self.pop25,
            'pop26': self.pop26,
            'live_births': self.live_births
        }

    # @classmethod
    # def find_by_year(cls, year):
    #     return cls.query.filter_by(year=year).all()

    # @classmethod
    # def find_by_sex(cls, sex):
    #     return cls.query.filter_by(sex=sex).all()

    # @classmethod
    # def find_by_country(cls, country_code):
    #     return cls.query.filter_by(country_code=country_code).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # @classmethod
    # def find__by_cys(cls, country_code, year, sex):
    #     # only one result should exist for this combination of variables - but just in case we return all
    #     # .order_by(int(cls.year))
    #     return cls.query.filter_by(country_code=country_code, year=year, sex=sex).all()

    @classmethod
    # make sure we pass a dictionary to this
    def search_populations(cls, kwargs):
        return cls.query.filter_by(**kwargs).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
