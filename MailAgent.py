#!/usr/bin/env python
# purpose of this class is listen to port and recieve smtp messages
# example of usage
# python3 MailAgent.py --host='127.0.0.1' --port=1025 to start listen to the specified port
import argparse
import asyncore
import getpass
import os
import os.path
import smtpd
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Config():
    KNOWN_DOMAIN = 'safebreach.com'
    TRIGGER_KEYWORD = 'banana'
    TEMP_FILE_PATH = '/root/hello'

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    # TODO to send mail we will need exisitng mail provider
    RESPONSE_EMAIL_FROM = 'a@a.com'
    SECRET_PASSWORD = 'secret password'


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Message Received from:', peer)
        print('From:', mailfrom)
        print('To  :', rcpttos)
        print('Message :', data)

        if is_known_domain(mailfrom):
            msg = process_data_and_get_message(data)
            send_email(Config.RESPONSE_EMAIL_FROM, 'Response from Mail Agent', msg)
        return


# TODO consider to verify more than just a name
def is_known_domain(domain):
    return Config.KNOWN_DOMAIN in domain


def process_data_and_get_message(mailData):
    if is_keyword_found(mailData):
        scriptPath = get_mail_attachment(mailData)
        if os.path.isfile(scriptPath):
            print('File exist')
            response = execute_file_as_python_script(scriptPath)
        else:
            response = 'Attachment missing'
    else:
        response = 'Invalid Keyword'
    return response


def is_keyword_found(mailData):
    return Config.TRIGGER_KEYWORD in mailData


# TODO find if we have attachments
def get_mail_attachment(mailData):
    return Config.TEMP_FILE_PATH


def execute_file_as_python_script(scriptPath):
    output = subprocess.check_call(scriptPath)
    return output


def send_email(sender, recipient, subject, message):
    print(sender)
    print(recipient)
    print(subject)
    print(message)
    """ Send email message """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = recipient
    msg['From'] = sender

    part = MIMEText('text', 'plain')
    part.set_payload(message)
    msg.attach(part)

    # create smtp session
    session = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    print(session.ehlo())
    print(session.starttls())
    #session.ehlo
    session.login(sender, Config.SECRET_PASSWORD)
    session.sendmail(sender, recipient, msg.as_string())
    print("Email sent.")
    session.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--host', action="store",
                        dest="host", type=str, required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    server = CustomSMTPServer((given_args.host, given_args.port), None)
    asyncore.loop()
