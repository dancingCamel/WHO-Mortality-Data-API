from flask import render_template, make_response, request, current_app, flash, redirect, url_for
from flask_restful import Resource
from flask_mail import Mail, Message
# from pprint import pprint
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Contact(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('contact.html'), 200, headers)

    def post(self):
        # get info from form
        subject = request.form.get("subject")
        message = request.form.get("message")
        name = request.form.get("name")
        email = request.form.get("email")

        # set up email config
        smtp_server = current_app.config['MAIL_SERVER']
        port = current_app.config['MAIL_PORT']
        sender_email = current_app.config['MAIL_DEFAULT_SENDER']
        mail_username = current_app.config['MAIL_USERNAME']
        receiver_email = current_app.config['MAIL_DEFAULT_SENDER']
        password = current_app.config['MAIL_PASSWORD']

        # set up mime message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        text = "A message from the contact form: " + \
            message + ". From: " + name + "(" + email + ")"
        html = "<h2>A message from the contact form</h2><p>" + \
            message + "</p><p>From: " + name + "(" + email + ")"

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        msg.attach(part1)
        msg.attach(part2)

        # Create a secure SSL context
        context = ssl.create_default_context()

        # try to send message and redirect to contact page
        # need to add local_hostname as the default hostname has an invalid character in it
        # TODO: change this for production
        with smtplib.SMTP(smtp_server, port=port, local_hostname="127.0.0.1") as server:
            try:
                server.starttls(context=context)
                server.login(mail_username, password)
                server.send_message(msg,
                                    sender_email, receiver_email)
                message = "Thank you for your message. We'll get back to you as soon as possible."
                flash(message, 'info')
            except Exception as e:
                # except Exception as e:
                error = "Sorry, your message could not be sent. Please try again later."
                flash(error, 'error')

        return redirect(url_for('contact'))
