from flask import render_template, make_response, Response, url_for
from flask_restful import Resource, Api


class Index(Resource):
    def get(self):
        # headers = {'Content-Type': 'text/html'}
        # return make_response(render_template(url_for('index')), 200, headers)

        # return url_for('api.index')
        return Response(render_template(url_for('index')), 200, mimetype='text/html')
        # pass
