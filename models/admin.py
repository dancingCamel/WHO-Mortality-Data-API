from db import db
from models.country import CountryModel


class AdminModel(db.Model):
    __tablename__ = 'admin_codes'

    id = db.Column(db.Integer, primary_key=True)
    admin_code = db.Column(db.String(5))
    country_code = db.Column(db.String(5))
    description = db.Column(db.String(80))

    def __init__(self, admin_code, country_code, description):
        self.admin_code = admin_code
        self.country_code = country_code
        self.description = description

    def json(self):
        country = CountryModel.find_by_code(self.country_code)
        if country:
            country = country.json()

        return {'code': self.admin_code,
                'country': country,
                'description': self.description
                }

    @classmethod
    def find_by_code_and_country(cls, admin_code, country_code):
        return cls.query.filter_by(admin_code=admin_code, country_code=country_code).first()

    @classmethod
    def find_by_code(cls, admin_code):
        return cls.query.filter_by(admin_code=admin_code).all()

    @classmethod
    def find_by_country(cls, country_code):
        return cls.query.filter_by(country_code=country_code).all()

    @classmethod
    def search_by_desc(cls, search_term):
        return cls.query.filter(cls.description.ilike('%' + search_term + '%')).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
