#!/usr/bin/env python
# purpose of this class is listen to port and recieve smtp messages
# example of usage
# python3 MailAgent.py --host='127.0.0.1' --port=1025
import argparse
import asyncore
import os.path
import smtpd
import subprocess


class Config():
    KNOWN_DOMAIN = "webname.com"
    TRIGGER_KEYWORD = "banana"
    TEMP_FILE_PATH = "/root/hello"


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Message Received from:', peer)
        print('From:', mailfrom)
        print('To  :', rcpttos)
        print('Message :', data)

        if isKnownDomain(mailfrom):
            msg = processDataAndGetMessage(data)
            sendEmail(mailfrom, msg)
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
# I will use google provider
def sendEmail(mailfrom, msg):
    print(mailfrom)
    print(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--host', action="store",
                        dest="host", type=str, required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    server = CustomSMTPServer((given_args.host, given_args.port), None)
    asyncore.loop()
