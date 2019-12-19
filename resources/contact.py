from flask import render_template, make_response
from flask_restful import Resource


class Contact(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('contact.html'), 200, headers)

    def post(self):
        # handle email sending here
        # get info from form
        # redirct to contact page with either an 'error' or a 'info' flash
        pass
