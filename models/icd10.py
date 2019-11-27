from db import db


class Icd10Model(db.Model):
    __tablename__ = 'icd10'

    id = db.Column(db.Integer, primary_key=True)
    code_list = db.Column(db.String(5))
    code = db.Column(db.String(5))
    description = db.Column(db.String(150))

    def __init__(self, code_list, code, description):
        self.code_list = code_list
        self.code = code
        self.description = description

    def json(self):
        return {
            'list': self.code_list,
            'code': self.code,
            'description': self.description
        }

    @classmethod
    def find_code_list(cls, code_list):
        return cls.query.filter_by(code_list=code_list).all()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).all()

    @classmethod
    def find_by_list_and_code(cls, code_list, code):
        # should only be able to find one entry
        return cls.query.filter_by(code_list=code_list, code=code).first()

    @classmethod
    def search(cls, search_term):
        return cls.query.filter(cls.description.ilike('%' + search_term + '%') | cls.code.ilike('%' + search_term + '%')).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
