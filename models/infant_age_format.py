from db import db


class InfantAgeFormatModel(db.Model):
    __tablename__ = 'infantAgeFormat'

    id = db.Column(db.Integer, primary_key=True)
    infant_age_format_code = db.Column(db.String(5))
    infantAge1 = db.Column(db.String(15))
    infantAge2 = db.Column(db.String(15))
    infantAge3 = db.Column(db.String(15))
    infantAge4 = db.Column(db.String(15))

    def __init__(self, infant_age_format_code, infantAge1, infantAge2, infantAge3, infantAge4):
        self.infant_age_format_code = infant_age_format_code
        self.infantAge1 = infantAge1
        self.infantAge2 = infantAge2
        self.infantAge3 = infantAge3
        self.infantAge4 = infantAge4

    def json(self):
        return {
            'infant_age_format_code': self.infant_age_format_code,
            'infant_age1': self.infantAge1,
            'infant_age2': self.infantAge2,
            'infant_age3': self.infantAge3,
            'infant_age4': self.infantAge4
        }

    @classmethod
    def find_by_code(cls, infant_age_format_code):
        return cls.query.filter_by(infant_age_format_code=infant_age_format_code).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
