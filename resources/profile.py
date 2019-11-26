from flask import render_template, url_for, make_response
from flask_restful import Resource
from flask_login import login_required


class Profile(Resource):
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('profile.html'), 200, headers)
