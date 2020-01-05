from db import db


class CodeListRefModel(db.Model):
    __tablename__ = 'code_list_ref'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4))
    country_code = db.Column(db.String(5))
    code_list = db.Column(db.String(5))

    def __init__(self, year, country_code, code_list):
        self.year = year
        self.country_code = country_code
        self.code_list = code_list

    def json(self):
        return {
            'year': self.year,
            'country_code': self.country_code,
            'code_list': self.code_list
        }

    @classmethod
    def find_by_year_and_country(cls, year, country_code):
        return cls.query.filter_by(year=year, country_code=country_code).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
