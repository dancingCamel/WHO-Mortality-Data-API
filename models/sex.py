from db import db


class SexModel(db.Model):
    __tablename__ = 'sex'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(20))
    sex_code = db.Column(db.String(5))

    def __init__(self, sex, sex_code):
        self.sex = sex
        self.sex_code = sex_code

    def json(self):
        return {'name': self.sex, 'code': self.sex_code}

    @classmethod
    def find_by_name(cls, sex):
        return cls.query.filter_by(sex=sex).first()

    @classmethod
    def find_by_code(cls, sex_code):
        return cls.query.filter_by(sex_code=sex_code).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
