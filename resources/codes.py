from flask import render_template, make_response, url_for
from flask_restful import Resource
from auth import requireApiKey
from flask_login import login_required


class Codes(Resource):
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('codes.html'), 200, headers)
