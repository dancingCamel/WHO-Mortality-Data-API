from flask import Flask
from flask_restful import Api
from db import db
from populate_data_tables import populate_country_table, populate_population_table, populate_sex_table
from resources.country import Country, CountryList, CountrySearch
from resources.sex import Sex, SexList
from resources.population import PopulationSearch, PopulationsList, PopulationOne, PopulationChange


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
    # only run these when first setting up the API
    # populate_country_table()
    # populate_population_table()
    # populate_sex_table()


api.add_resource(Country, '/api/country/<string:country_name>')
api.add_resource(CountryList, '/api/country-list')
api.add_resource(CountrySearch, '/api/country-search/<string:search_term>')
api.add_resource(Sex, '/api/sex/<string:sex>')
api.add_resource(SexList, '/api/sex-list/')
api.add_resource(PopulationSearch, '/api/population-search')
api.add_resource(PopulationOne, '/api/population-one')
api.add_resource(PopulationsList, '/api/population-list')
api.add_resource(
    PopulationChange, '/api/population-change/<string:country_code>/<string:year>/<string:sex>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
