from flask_restful import Resource
from auth import requireApiKey


class Info(Resource):
    @requireApiKey
    def get(self):
        return {
            "title": "WHO Mortality Database API",
            "description": "Query the WHO Mortality database data.",
            "disclaimer": "Every attempt has been made to keep data true to the original raw data files but veracity cannot be guaranteed. If this is important, download the data directly or use https://www.who.int/healthinfo/mortality_data/en/ data querying services. All analyses, interpretations or conclusions drawn from this API or found on this website are credited to the authors, not the WHO (which is responsible only for the provision of the original information). For more information visit https://www.who.int/healthinfo/statistics/mortality_rawdata/en/",
            "contact": {
                "name": "App Support",
                "url": "http://www.whomortalitydatabase.com/contact",
                "email": "whomortalitydatabase@gmail.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "version": "1.0.0"
        }
