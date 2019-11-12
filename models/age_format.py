from db import db


class AgeFormatModel(db.Model):
    __tablename__ = 'ageformat'

    id = db.Column(db.Integer, primary_key=True)
    age_format_code = db.Column(db.String(5))
    # skip pop1 as pop1 is all_ages which is in every age format and not required for age breakdowns
    pop2 = db.Column(db.String(15))
    pop3 = db.Column(db.String(15))
    pop4 = db.Column(db.String(15))
    pop5 = db.Column(db.String(15))
    pop6 = db.Column(db.String(15))
    pop7 = db.Column(db.String(15))
    pop8 = db.Column(db.String(15))
    pop9 = db.Column(db.String(15))
    pop10 = db.Column(db.String(15))
    pop11 = db.Column(db.String(15))
    pop12 = db.Column(db.String(15))
    pop13 = db.Column(db.String(15))
    pop14 = db.Column(db.String(15))
    pop15 = db.Column(db.String(15))
    pop16 = db.Column(db.String(15))
    pop17 = db.Column(db.String(15))
    pop18 = db.Column(db.String(15))
    pop19 = db.Column(db.String(15))
    pop20 = db.Column(db.String(15))
    pop21 = db.Column(db.String(15))
    pop22 = db.Column(db.String(15))
    pop23 = db.Column(db.String(15))
    pop24 = db.Column(db.String(15))
    pop25 = db.Column(db.String(15))
    pop26 = db.Column(db.String(15))

    def __init__(self, age_format_code, pop2, pop3, pop4, pop5, pop6, pop7, pop8, pop9, pop10, pop11, pop12, pop13, pop14, pop15, pop16, pop17, pop18, pop19, pop20, pop21, pop22, pop23, pop24, pop25, pop26):
        self.age_format_code = age_format_code
        self.pop2 = pop2
        self.pop3 = pop3
        self.pop4 = pop4
        self.pop5 = pop5
        self.pop6 = pop6
        self.pop7 = pop7
        self.pop8 = pop8
        self.pop9 = pop9
        self.pop10 = pop10
        self.pop11 = pop11
        self.pop12 = pop12
        self.pop13 = pop13
        self.pop14 = pop14
        self.pop15 = pop15
        self.pop16 = pop16
        self.pop17 = pop17
        self.pop18 = pop18
        self.pop19 = pop19
        self.pop20 = pop20
        self.pop21 = pop21
        self.pop22 = pop22
        self.pop23 = pop23
        self.pop24 = pop24
        self.pop25 = pop25
        self.pop26 = pop26

    def json(self):
        return {
            'age_format_code': self.age_format_code,
            'pop2': self.pop2,
            'pop3': self.pop3,
            'pop4': self.pop4,
            'pop5': self.pop5,
            'pop6': self.pop6,
            'pop7': self.pop7,
            'pop8': self.pop8,
            'pop9': self.pop9,
            'pop10': self.pop10,
            'pop11': self.pop11,
            'pop12': self.pop12,
            'pop13': self.pop13,
            'pop14': self.pop14,
            'pop15': self.pop15,
            'pop16': self.pop16,
            'pop17': self.pop17,
            'pop18': self.pop18,
            'pop19': self.pop19,
            'pop20': self.pop20,
            'pop21': self.pop21,
            'pop22': self.pop22,
            'pop23': self.pop23,
            'pop24': self.pop24,
            'pop25': self.pop25,
            'pop26': self.pop26,
        }

    @classmethod
    def find_by_code(cls, age_format_code):
        return cls.query.filter_by(age_format_code=age_format_code).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
