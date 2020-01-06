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
                                  populate_icd_table_101,
                                  populate_icd_table_103,
                                  populate_icd_table_104,
                                  populate_icd_table_10M,
                                  populate_icd_table_UE1,
                                  populate_icd_code_lists_table,
                                  populate_mortality_table,
                                  populate_code_list_reference)
from models.user import UserModel
from resources.country import CountryCode, CountryList, CountrySearch, CountryDesc, CountryName
from resources.sex import SexCode, SexList, SexDesc
from resources.population import PopulationSearch, PopulationsList, PopulationOne, PopulationChange, PopulationSearchMultiple
from resources.admin import Admin, AdminList, AdminCode, AdminDesc, AdminSearch
from resources.subdiv import SubdivCode, SubdivList, SubdivDesc, SubdivSearch
from resources.age_format import AgeFormatCode, AgeFormatList
from resources.infant_age_format import InfantAgeFormatCode, InfantAgeFormatList
from resources.icd import Icd, IcdList, IcdSearch, IcdCode, IcdDesc
from resources.icd_lists import IcdCodeListCode, IcdCodeListDesc, IcdAllCodeLists
from resources.mortality import MortalityDataSearch, MortalityDataOne, MortalityDataChange, MortalitySearchMultiple
from resources.mortality_adj import MortalityAdjustedSearch, MortalityAdjustedOne, MortalityAdjustedSearchMultiple
from resources.user import UserRegister, User, UserLogin, UserLogout, UserApiKey, UserPassword
from resources.superuser import Superuser, SuperuserUpdate
from models.superuser import SuperuserModel
from resources.index import Index
from resources.profile import Profile
from resources.docs import Docs
from resources.visualize import Visualize
from resources.codes import Codes
from resources.contact import Contact
from resources.jsonpage import Json
from resources.info import Info
from resources.externalDocs import ExternalDocs
from resources.paths import Paths
from db import db
import os

app = Flask(__name__)
api = Api(app)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# error handling
app.config['PROPAGATE_EXCEPTIONS'] = True
# secret key for development
app.secret_key = "dev"
# production
app.config.from_pyfile('config.py', silent=True)

# Flask login config
login_manager = LoginManager()
login_manager.login_view = 'userlogin'
login_manager.init_app(app)
login_manager.refresh_view = "userlogin"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate."
)
login_manager.needs_refresh_message_category = "info"

# mail configuration
app.config['DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False


@login_manager.user_loader
def load_user(user_id):
    return UserModel.find_by_id(user_id)

# uncomment these to populate all tables first time run programme
# moved to run file for production.
@app.before_first_request
def create_tables():
    db.create_all()
    # populate_code_list_reference()
    # populate_country_table()
    # populate_population_table()
    # populate_sex_table()
    # populate_admin_table()
    # populate_subdiv_table()
    # populate_age_format_table()
    # populate_infant_age_format_table()
    #     populate_icd_table_101()
    #     populate_icd_table_103()
    #     populate_icd_table_104()
    #     populate_icd_table_10M()
    #     populate_icd_table_UE1()
    # populate_icd_code_lists_table()


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

# ICD code endpoints
api.add_resource(Icd, '/api/icd/<string:code_list>/<string:code>')
api.add_resource(IcdList, '/api/icd-list')
api.add_resource(IcdSearch, '/api/icd-search/<string:search_term>')
# ICD endpoints specifically for browser based search
api.add_resource(IcdDesc, '/api/icd-desc/<string:search_term>')
api.add_resource(IcdCode, '/api/icd-code/<string:code>')

# ICD code list endpoints
api.add_resource(IcdCodeListCode, '/api/icd-code-list-code/<string:code>')
api.add_resource(IcdCodeListDesc,
                 '/api/icd-code-list-desc/<string:search_term>')
api.add_resource(IcdAllCodeLists, '/api/icd-code-list-list')

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

# API info endpoinds
api.add_resource(Info, '/api/info')
api.add_resource(ExternalDocs, '/api/externalDocs')
api.add_resource(Paths, '/api/paths')


# remove for deployment
# db.init_app(app)

# allow to run either by flask run or app.py
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        app.run(host="127.0.0.1", port=5000, debug=True)

#  remove this for deployment


# def create_app():
#     with app.app_context():
#         db.init_app(app)
#         return app
