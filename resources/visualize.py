from flask import render_template, make_response, url_for
from flask_restful import Resource


class Visualize(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('visualize.html'), 200, headers)