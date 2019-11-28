from flask import render_template, make_response, url_for
from flask_restful import Resource
from flask_login import login_required


class Json(Resource):
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('json.html'), 200, headers)