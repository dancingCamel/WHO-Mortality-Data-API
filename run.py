from app import app
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
                                  populate_mortality_table)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
    # don't run populate table functions on remote server as timeout
    populate_country_table()
    populate_population_table()
    populate_sex_table()
    populate_admin_table()
    populate_subdiv_table()
    populate_age_format_table()
    populate_infant_age_format_table()
    populate_icd_table_101()
    populate_icd_table_103()
    populate_icd_table_104()
    populate_icd_table_10M()
    populate_icd_table_UE1()
    populate_icd_code_lists_table()
