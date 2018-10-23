#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import syslog
import telegram
from abc import abstractmethod


class Sender:
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def send(self):
        pass


class SendSMS(Sender):
    def send(self):
        smsDict = json.loads(self.data)

        number = smsDict['number']
        subject = smsDict['subject']
        message = smsDict['message']

        message = subject + " " + message
        message = message.replace('\n', '')
        message = message[:70].encode('utf-8')

        try:
            connection = dbModule.Connection("db_login/db_pass")
            cursor = connection.cursor()

            sql = "DECLARE res_v VARCHAR (100); \
                BEGIN send_procedure(%s, %s); COMMIT; END;" \
                  % (number.encode('utf-8'), message)

            cursor.execute(sql)

            syslog.syslog("Sending SMS message to: %s" % (smsDict['number']))
        except Exception as exc:
            syslog.syslog("Error while sending SMS notification: %s" % (exc))

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


class SendTelegram(Sender):
    def send(self):
        try:
            # Telegram Bot
            pp = telegram.utils.request.Request(proxy_url='socks5://0.0.0.0:9999', urllib3_proxy_kwargs={
                'username': 'some_username', 'password': 'some_password'})
            bot = telegram.Bot(
                token='id:token', request=pp)

            telegramData = json.loads(self.data)
            bot.sendMessage(telegramData['channel'], telegramData['message'])
        except Exception as exc:
            syslog.syslog("Error while sending telegram: %s" % (exc))


class SendMail(Sender):
    def send(self):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.header import Header
        from validate_email import validate_email

        try:
            my_mail = 'mail@mail.server'
            mailDict = json.loads(self.data)
            mail_is_valid = validate_email(mailDict['mail'])

            if mail_is_valid is not True:
                raise Exception("invalid e-mail: " + mailDict['mail'])

            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(mailDict['subject'], 'utf-8')
            msg['From'] = my_mail
            msg['To'] = mailDict['mail']

            msgText = MIMEText(mailDict['message'].encode(
                'utf-8'), 'plain', 'utf-8')
            msg.attach(msgText)

            s = smtplib.SMTP('mail.server')
            s.sendmail(my_mail, mailDict['mail'], msg.as_string())

            syslog.syslog("Sending email-massage to: %s" % (mailDict['mail']))
        except Exception as exc:
            syslog.syslog("Error while sending e-mail: %s" % (exc))

        finally:
            if s:
                s.quit()
