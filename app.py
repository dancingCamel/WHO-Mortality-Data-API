from flask import Flask
from flask_restful import Api
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


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# secret key for development
app.secret_key = "dev"
# production
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
    # populate_mortality_table()


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

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
