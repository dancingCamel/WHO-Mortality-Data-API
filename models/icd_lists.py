from db import db


class IcdListsModel(db.Model):
    __tablename__ = 'icd_lists'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    description = db.Column(db.String(80))

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def json(self):
        return {
            'list': self.code,
            'description': self.description
        }

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

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
