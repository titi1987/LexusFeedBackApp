from flask import Flask, render_template, request
import os
import ssl
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Feedback():
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

def send_email(customer, dealer, rating, comments):
    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "lipot.pcikermann@gmail.com"  # Enter your address
    receiver_email = "titooo1987123@gmail.com"  # Enter receiver address
    password = "London861022@@" # Enter your app password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Lexus Feedback"
    message["From"] = sender_email
    message["To"] = receiver_email
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        # Print any error messages to stdout
        print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        feedback = Feedback(customer, dealer, rating, comments)
        send_email(customer, dealer, rating, comments)
        return render_template('success.html')

if __name__ == '__main__':
    app.run()
