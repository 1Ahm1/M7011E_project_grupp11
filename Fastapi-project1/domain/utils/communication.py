import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#ToDo: replace with email and app password
EMAIL_SENDER = "librarymanager.se@gmail.com"
PASSWORD = "jirf ctiz ieia zupd"

def send_mail(user_email: str, subject: str, body: str):
    if EMAIL_SENDER and PASSWORD:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = user_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your domain's SMTP server and port
        server.starttls()
        server.login(EMAIL_SENDER, PASSWORD)
        server.send_message(msg)
        server.quit()

def verification_code(user_email: str, code: int):
    subject = "Verification Code"
    body = f"""
    Hello,

    Thank you for using our site! Your verification code is:
    
    {code}
    
    Please enter this code into the browser app to verify your account.

    If you did not request this verification code, please disregard this message.

    Thank you,

    """
    send_mail(user_email, subject, body)

def purchase_confirmation(user_email: str, order: int):
    subject = "Purchase Confirmation"
    body = f"""
    Hello,

    Your order no. {order} has been pruchase successfully.

    """
    send_mail(user_email, subject, body)
