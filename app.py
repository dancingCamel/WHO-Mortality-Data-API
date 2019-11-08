from flask import Flask
from flask_restful import Api
from db import db
from populate_data_tables import populate_country_table, populate_population_table
from resources.country import Country, CountryList, CountrySearch
from resources.sex import Sex


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
    populate_country_table()
    populate_population_table()


api.add_resource(Country, '/api/country/<string:country_name>')
api.add_resource(CountryList, '/api/countries')
api.add_resource(CountrySearch, '/api/country-search/<string:search_term>')
api.add_resource(Sex, '/api/sex/<string:sex>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
