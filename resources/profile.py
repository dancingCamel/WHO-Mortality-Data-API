from flask import render_template
from flask_restful import Resource


class Profile(Resource):
    def get(self):
        return render_template('profile.html')
