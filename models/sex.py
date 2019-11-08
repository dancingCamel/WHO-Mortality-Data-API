from codes import sex_codes


class SexModel():

    def __init__(self, sex, sex_code):
        self.sex = sex
        self.sex_code = sex_code

    @classmethod
    def find_code(cls, sex):
        return {'sex': sex, 'sex_code': sex_codes[sex]}
