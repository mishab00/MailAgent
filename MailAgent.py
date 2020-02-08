#!/usr/bin/env python
# purpose of this class is listen to port and recieve smtp messages
# example of usage
# python3 MailAgent.py --host='127.0.0.1' --port=1025
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
    KNOWN_DOMAIN = "webname.com"
    TRIGGER_KEYWORD = "banana"
    TEMP_FILE_PATH = "/root/hello"

    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    RESPONSE_EMAIL_FROM = "a@a.com"


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Message Received from:', peer)
        print('From:', mailfrom)
        print('To  :', rcpttos)
        print('Message :', data)

        if isKnownDomain(mailfrom):
            msg = processDataAndGetMessage(data)
            sendEmail(Config.RESPONSE_EMAIL_FROM, "Response from Mail Agent", msg)
        return


# TODO consider to verify more than just a name
def isKnownDomain(domain):
    return Config.KNOWN_DOMAIN in domain


def processDataAndGetMessage(mailData):
    if isKeywordFound(mailData):
        scriptPath = getMailAttachment(mailData)
        if os.path.isfile(scriptPath):
            print('File exist')
            response = executeFileAsPythonScript(scriptPath)
        else:
            response = 'Attachment missing'
    else:
        response = 'Invalid Keyword'
    return response


def isKeywordFound(mailData):
    return Config.TRIGGER_KEYWORD in mailData


# TODO find if we have attachments
def getMailAttachment(mailData):
    return Config.TEMP_FILE_PATH


def executeFileAsPythonScript(scriptPath):
    output = subprocess.check_call(scriptPath)
    return output


# TODO to send mail we will need exisitng mail provider
def sendEmail(sender, recipient, subject, message):
    print(sender)
    print(recipient)
    print(subject)
    print(message)
    """ Send email message """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = recipient
    msg['From'] = sender

    part = MIMEText('text', "plain")
    part.set_payload(message)
    msg.attach(part)

    # create smtp session
    session = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo
    password = getpass.getpass(prompt="Enter your Google password: ")
    session.login(sender, "Secret Password")
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
