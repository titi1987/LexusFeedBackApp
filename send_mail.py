import os
import ssl
import smtplib
from email.message import EmailMessage


def send_email(feedback):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get('SENDER_EMAIL')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    password = os.environ.get('SENDER_PASSWORD')
    context = ssl.create_default_context()

    message = EmailMessage()
    message['Subject'] = 'New Feedback Submitted'
    message['From'] = sender_email
    message['To'] = receiver_email
    message.set_content(f'''New feedback has been submitted:
    Customer: {feedback.customer}
    Dealer: {feedback.dealer}
    Rating: {feedback.rating}
    Comments: {feedback.comments}
    ''')

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(message)