from db import db


class BlacklistModel(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(80))

    def __init__(self, api_key):
        self.api_key = api_key

    def json(self):
        return {'api_key': self.api_key}

    @classmethod
    def find_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()
