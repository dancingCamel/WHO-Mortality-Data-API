from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
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
from resources.country import Country, CountryList, CountrySearch
from resources.sex import Sex, SexList
from resources.population import PopulationSearch, PopulationsList, PopulationOne, PopulationChange
from resources.admin import Admin, AdminList
from resources.subdiv import Subdiv, SubdivList
from resources.age_format import AgeFormat, AgeFormatList
from resources.infant_age_format import InfantAgeFormat, InfantAgeFormatList
from resources.icd10 import Icd10, Icd10List, Icd10Search
from resources.icd10_lists import Icd10CodeList, Icd10AllCodeLists
from resources.mortality import MortalityDataSearch, MortalityDataOne, MortalityDataChange
from resources.mortality_adj import MortalityAdjustedSearch, MortalityAdjustedOne
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.superuser import Superuser, SuperuserUpdate
from models.superuser import SuperuserModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# JWT error handling
app.config['PROPAGATE_EXCEPTIONS'] = True
# enable blacklisting
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# secret key for development
app.secret_key = "dev"
# production
app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('config.py', silent=True)

api = Api(app)


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


jwt = JWTManager(app)  # /auth


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = SuperuserModel.find_by_user_id(identity)
    if user:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
# function to return true if in blacklist
def check_if_token_in_blacklist(decrypted_token):
    # return true or false. if true it will jump to revoked token loader
    return decrypted_token['jti'] in BLACKLIST

# custom error messages
@jwt.expired_token_loader
# do this when token expires
def expired_token_callback(error):
    return jsonify({
        'description': "The token has expired.",
        'error': "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({
        'description': 'This token is not fresh',
        'error': 'fresh_token_required'
    }), 401

# revoke token when log out or if hit usage limits
@jwt.revoked_token_loader
def revoked_token_callback(error):
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


api.add_resource(Country, '/api/country/<string:country_name>')
api.add_resource(CountryList, '/api/country-list')
api.add_resource(CountrySearch, '/api/country-search/<string:search_term>')
api.add_resource(Sex, '/api/sex/<string:sex>')
api.add_resource(SexList, '/api/sex-list/')
api.add_resource(Admin, '/api/admin/<string:admin_code>/<string:country_code>')
api.add_resource(AdminList, '/api/admin-list')
api.add_resource(Subdiv, '/api/subdiv/<string:subdiv_code>')
api.add_resource(SubdivList, '/api/subdiv-list')
api.add_resource(AgeFormat, '/api/age-format/<string:age_format_code>')
api.add_resource(AgeFormatList, '/api/age-format-list')
api.add_resource(
    InfantAgeFormat, '/api/infant-age-format/<string:infant_age_format_code>')
api.add_resource(InfantAgeFormatList, '/api/infant-age-format-list')
api.add_resource(PopulationSearch, '/api/population-search')
api.add_resource(PopulationOne, '/api/population-one')
api.add_resource(PopulationsList, '/api/population-list')
api.add_resource(
    PopulationChange, '/api/population-change/<string:country_code>/<string:year>/<string:sex>')
api.add_resource(Icd10, '/api/icd10/<string:code_list>/<string:code>')
api.add_resource(Icd10List, '/api/icd10-list')
api.add_resource(Icd10Search, '/api/icd10-search/<string:search_term>')
api.add_resource(Icd10CodeList, '/api/icd10-code-list/<string:code>')
api.add_resource(Icd10AllCodeLists, '/api/icd10-code-lists')
api.add_resource(MortalityDataSearch, '/api/mortality-data-search')
api.add_resource(MortalityDataOne, '/api/mortality-data-one')
api.add_resource(MortalityDataChange,
                 '/api/mortality-data-change/<string:country_code>/<string:year>/<string:sex>/<string:cause>')
api.add_resource(MortalityAdjustedSearch, '/api/mortality-adj-search')
api.add_resource(MortalityAdjustedOne, '/api/mortality-adj-one')

# user endpoints
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
# api.add_resource(Profile, '/profile')

# superuser endpoints
api.add_resource(Superuser, '/superuser/<string:username>')
api.add_resource(SuperuserUpdate, '/superuser-update')

# site endpoints
# api.add_resource(Visualize, '/visualize')
# api.add_resource(Index, '/')
# api.add_resource(Docs '/docs')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
