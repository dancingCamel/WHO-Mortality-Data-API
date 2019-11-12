from db import db
from sqlalchemy import func


class CountryModel(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(5))
    country_name = db.Column(db.String(80))

    def __init__(self, country_code, country_name):
        self.country_code = country_code
        self.country_name = country_name

    def json(self):
        return {
            'code': self.country_code,
            'name': self.country_name
        }

    @classmethod
    def find_by_code(cls, country_code):
        return cls.query.filter_by(country_code=country_code).first()

    @classmethod
    def find_by_name(cls, country_name):
        return cls.query.filter(cls.country_name.ilike(country_name)).first()

    @classmethod
    def search_by_name(cls, search_term):
        return cls.query.filter(cls.country_name.ilike('%' + search_term + '%')).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
