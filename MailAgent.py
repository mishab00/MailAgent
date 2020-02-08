#!/usr/bin/env python
#purpose of this class is listen to port and recieve smtp messages
#example of usage
#python3 MailAgent.py --host='127.0.0.1' --port=1025
import smtpd
import asyncore
import argparse
import os.path


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Message Received from:', peer)
        print('From:', mailfrom)
        print('To  :', rcpttos)
        print('Message :', data)

        if (isKnownDomain(mailfrom)):
            msg = processDataAndGetMessage(data)
            sendEmail(mailfrom, msg)
        return


# TODO verify domain is meet the policy
def isKnownDomain(domain):
    return True


def processDataAndGetMessage(mailData):
    if (isKeywordFound(mailData)):
        scriptPath = getMailAttachment(mailData)
        if os.path.isfile(scriptPath):
            print('File exist')
            response = executeFileAsPythonScript(scriptPath)
        else:
            response = 'Attachment missing'
    else:
        response = 'Invalid Keyword'
    return response


# TODO parse data and find keyword
def isKeywordFound(mailData):
    return True


# TODO find if we have attachments
def getMailAttachment(mailData):
    return '/path/to/Attachment'


# TODO execute python script and collect output or exception if persist
def executeFileAsPythonScript(scriptPath):
    return 'Response or Exception from the script'


def sendEmail(mailfrom, msg):
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--host', action="store",
                        dest="host", type=str, required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    server = CustomSMTPServer((given_args.host, given_args.port), None)
    asyncore.loop()
