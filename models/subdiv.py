from db import db


class SubdivModel(db.Model):
    __tablename__ = 'subdiv'
    id = db.Column(db.Integer, primary_key=True)
    subdiv_code = db.Column(db.String(5))
    description = db.Column(db.String(50))

    def __init__(self, subdiv_code, description):
        self.subdiv_code = subdiv_code
        self.description = description

    def json(self):
        return {'code': self.subdiv_code, 'description': self.description}

    @classmethod
    def find_by_code(cls, subdiv_code):
        return cls.query.filter_by(subdiv_code=subdiv_code).first()

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
