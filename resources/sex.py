from flask_restful import Resource
from models.sex import SexModel


class Sex(Resource):
    def get(self, sex):
        return SexModel.find_by_name(sex)
