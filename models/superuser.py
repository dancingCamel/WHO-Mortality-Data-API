from db import db

# use superuser instead of admin as admin is used extensively elsewhere in the API


class SuperuserModel(db.Model):
    __tablename__: 'superusers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

    def __init__(self, username):
        self.username = username

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
