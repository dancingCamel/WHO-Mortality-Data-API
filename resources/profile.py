from flask import render_template, url_for, make_response
from flask_restful import Resource


class Profile(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('profile.html'), 200, headers)
