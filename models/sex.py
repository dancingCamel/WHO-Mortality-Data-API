from codes import sex_codes


class SexModel():

    def __init__(self, sex, sex_code):
        self.sex = sex
        self.sex_code = sex_code

    @classmethod
    def find_by_name(cls, sex):
        # error handling
        if sex in sex_codes:
            return {'sex': sex, 'sex_code': sex_codes[sex]}
        return None

    @classmethod
    def find_by_code(cls, sex_code):
        if sex_code in sex_codes.values():
            for sex, code in sex_codes.items():
                if code == sex_code:
                    return {'sex': sex, 'sex_code': sex_code}
        return None
