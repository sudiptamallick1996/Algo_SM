from .email_config import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def setup_send_email(smtp_server, smtp_port, smtp_username, smtp_password, message):
    smtp_username = sender_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            print("SMTP server login successful")
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(e)   

def create_email(body_content):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Updates from Algo SM"
    body = body_content
    message.attach(MIMEText(body, "plain"))

    return message

def send_email(message):
    message = create_email(body_content = message)
    setup_send_email(smtp_server, smtp_port, sender_email, smtp_password, message)