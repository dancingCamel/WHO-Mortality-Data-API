from flask_restful import Resource
from auth import requireApiKey


class ExternalDocs(Resource):
    @requireApiKey
    def get(self):
        return {
            "description": "Find more info here",
            "url": "https://www.whomortalitydatabase.com/docs"
        }
