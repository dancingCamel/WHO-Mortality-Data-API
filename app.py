from flask import Flask, jsonify, request, abort
from flask_restful import Api
from flask_login import LoginManager
from db import db
from populate_data_tables import (populate_country_table,
                                  populate_population_table,
                                  populate_sex_table,
                                  populate_admin_table,
                                  populate_subdiv_table,
                                  populate_age_format_table,
                                  populate_infant_age_format_table,
                                  populate_icd10_table_101,
                                  populate_icd10_table_103,
                                  populate_icd10_table_104,
                                  populate_icd10_table_10M,
                                  populate_icd10_table_UE1,
                                  populate_icd10_code_lists_table,
                                  populate_mortality_table)
from models.user import UserModel
from resources.country import CountryCode, CountryList, CountrySearch, CountryDesc, CountryName
from resources.sex import SexCode, SexList, SexDesc
from resources.population import PopulationSearch, PopulationsList, PopulationOne, PopulationChange, PopulationSearchMultiple
from resources.admin import Admin, AdminList, AdminCode, AdminDesc, AdminSearch
from resources.subdiv import SubdivCode, SubdivList, SubdivDesc, SubdivSearch
from resources.age_format import AgeFormatCode, AgeFormatList
from resources.infant_age_format import InfantAgeFormatCode, InfantAgeFormatList
from resources.icd10 import Icd10, Icd10List, Icd10Search, Icd10Code, Icd10Desc
from resources.icd10_lists import Icd10CodeListCode, Icd10CodeListDesc, Icd10AllCodeLists
from resources.mortality import MortalityDataSearch, MortalityDataOne, MortalityDataChange, MortalitySearchMultiple
from resources.mortality_adj import MortalityAdjustedSearch, MortalityAdjustedOne, MortalityAdjustedSearchMultiple
# from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, UserLogout, UserApiKey, UserPassword
from resources.superuser import Superuser, SuperuserUpdate
from models.superuser import SuperuserModel
from resources.index import Index
from resources.profile import Profile
from resources.docs import Docs
from resources.visualize import Visualize
from resources.codes import Codes
from resources.contact import Contact
from resources.json import Json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# error handling
app.config['PROPAGATE_EXCEPTIONS'] = True


# secret key for development
app.secret_key = "dev"
# production
app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('config.py', silent=True)

api = Api(app)
login_manager = LoginManager()
login_manager.login_view = 'userlogin'
login_manager.init_app(app)
login_manager.refresh_view = "userlogin"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate."
)
login_manager.needs_refresh_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(user_id)


@app.before_first_request
def create_tables():
    db.create_all()
    # populate table function. auto skips if table exists
    populate_country_table()
    populate_population_table()
    populate_sex_table()
    populate_admin_table()
    populate_subdiv_table()
    populate_age_format_table()
    populate_infant_age_format_table()
    populate_icd10_table_101()
    populate_icd10_table_103()
    populate_icd10_table_104()
    populate_icd10_table_10M()
    populate_icd10_table_UE1()
    populate_icd10_code_lists_table()
    # mortality data csv is too large. need to use sqlite3 .import function
    # populate_mortality_table()


# Country endpoints
api.add_resource(CountryCode, '/api/country-code/<string:country_code>')
api.add_resource(CountryName, '/api/country-name/<string:country_name>')
api.add_resource(CountryList, '/api/country-list')
api.add_resource(CountrySearch, '/api/country-search/<string:search_term>')
# replicate search endpoint specifically for browser page search
api.add_resource(CountryDesc, '/api/country-desc/<string:search_term>')

# Sex endpoints
api.add_resource(SexCode, '/api/sex-code/<string:sex_code>')
api.add_resource(SexDesc, '/api/sex-desc/<string:sex>')
api.add_resource(SexList, '/api/sex-list/')

# 'Admin' endpoints
api.add_resource(Admin, '/api/admin/<string:admin_code>/<string:country_code>')
api.add_resource(AdminList, '/api/admin-list')
api.add_resource(AdminCode, '/api/admin-code/<string:admin_code>')
api.add_resource(AdminDesc, '/api/admin-desc/<string:search_term>')
api.add_resource(AdminSearch, '/api/admin-search/<string:search_term>')

# Subdiv endpoints
api.add_resource(SubdivCode, '/api/subdiv-code/<string:subdiv_code>')
api.add_resource(SubdivDesc, '/api/subdiv-desc/<string:search_term>')
api.add_resource(SubdivSearch, '/api/subdiv-search/<string:search_term>')
api.add_resource(SubdivList, '/api/subdiv-list')

# Age format endpoints
api.add_resource(
    AgeFormatCode, '/api/age-format-code/<string:age_format_code>')
api.add_resource(AgeFormatList, '/api/age-format-list')
api.add_resource(
    InfantAgeFormatCode, '/api/infant-age-format-code/<string:infant_age_format_code>')
api.add_resource(InfantAgeFormatList, '/api/infant-age-format-list')

# Population endpoints
api.add_resource(PopulationSearch, '/api/population-search')
api.add_resource(PopulationOne, '/api/population-one')
api.add_resource(PopulationsList, '/api/population-list')
api.add_resource(
    PopulationChange, '/api/population-change/<string:country_code>/<string:year>/<string:sex>')
api.add_resource(PopulationSearchMultiple, '/api/population-search-multiple')

# ICD10 code endpoints
api.add_resource(Icd10, '/api/icd10/<string:code_list>/<string:code>')
api.add_resource(Icd10List, '/api/icd10-list')
api.add_resource(Icd10Search, '/api/icd10-search/<string:search_term>')
# ICD10 endpoints specifically for browser based search
api.add_resource(Icd10Desc, '/api/icd10-desc/<string:search_term>')
api.add_resource(Icd10Code, '/api/icd10-code/<string:code>')

# ICD code list endpoints
api.add_resource(Icd10CodeListCode, '/api/icd10-code-list-code/<string:code>')
api.add_resource(Icd10CodeListDesc,
                 '/api/icd10-code-list-desc/<string:search_term>')
api.add_resource(Icd10AllCodeLists, '/api/icd10-code-lists')

# Mortality data endpoints
api.add_resource(MortalityDataSearch, '/api/mortality-data-search')
api.add_resource(MortalityDataOne, '/api/mortality-data-one')
api.add_resource(MortalityDataChange,
                 '/api/mortality-data-change/<string:country_code>/<string:year>/<string:sex>/<string:cause>')
api.add_resource(MortalityAdjustedSearch, '/api/mortality-adj-search')
api.add_resource(MortalityAdjustedSearchMultiple,
                 '/api/mortality-adj-search-multiple')
api.add_resource(MortalityAdjustedOne, '/api/mortality-adj-one')
api.add_resource(MortalitySearchMultiple, '/api/mortality-search-multiple')

# user endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserApiKey, '/newApiKey')
api.add_resource(UserPassword, '/changePass')
# api.add_resource(TokenRefresh, '/refresh')

# superuser endpoints
api.add_resource(Superuser, '/superuser/<string:username>')
api.add_resource(SuperuserUpdate, '/superuser-update')

# site endpoints
api.add_resource(Index, '/')
api.add_resource(Visualize, '/visualize')
api.add_resource(Docs, '/docs')
api.add_resource(Json, '/json')
api.add_resource(Codes, '/codes')
api.add_resource(Profile, '/profile')
api.add_resource(Contact, '/contact')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
