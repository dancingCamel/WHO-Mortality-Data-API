from flask import render_template, make_response, url_for, Markup, flash
from flask_restful import Resource


class Index(Resource):
    def get(self):
        message = Markup("<br><br><h3>{'message': 'this is a message'}</h3>")
        flash(message)
        error = "There was an error"
        flash(error)
        headers = {'Content-Type': 'text/html'}
        # return make_response(render_template(url_for('index')), 200, headers)
        return make_response(render_template('index.html', message=message), 200, headers)

