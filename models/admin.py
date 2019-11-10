from codes import admin_codes


class AdminModel():

    def __init__(self, admin_code, country_code, description):
        self.admin_code = admin_code
        self.country_code = country_code
        self.description = description

    @classmethod
    def find_by_code_and_country(cls, admin_code, country_code):
        # error handling
        if admin_code in admin_codes:
            if country_code in admin_codes[admin_code]:
                return {'admin_code': admin_code, 'country': country_code, 'area': admin_codes[admin_code][country_code]}
        return None

    @classmethod
    def find_by_code(cls, admin_code):
        if admin_code in admin_codes:
            for admin_code in admin_codes:
                countries_with_admin_code = []
                for country_code in admin_codes[admin_code]:
                    countries_with_admin_code.append(country_code)
                return {'admin_code': admin_code, 'countries': countries_with_admin_code}
        return None
