#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import sys
import json
import syslog
import time
import telegram
from threading import Thread


from .start_consume import Consume
from .callback import CallbackDbOne, CallbackDbTwo, CallbackDbThree
from .send import SendMail, SendSMS, SendTelegram


class Supervisor:
    _thr = []

    @classmethod
    def start_threads(cls, thread_list):

        for thread_name in thread_list:
            cls._thr.append(None)  # )))

        while True:
            i = 0

            for thread_name in thread_list:
                if not cls._thr[i] or not cls._thr[i].is_alive():
                    cls._thr[i] = Thread(target=thread_name)
                    cls._thr[i].daemon = True
                    cls._thr[i].start()
                    syslog.syslog("Starting thread for: %s" % str(thread_name))
                    cls._thr[i].join(1)
                i = i + 1

            time.sleep(10)


class TelegramAPI:
    def __init__(self, token, proxy={}):
        self.BOT_TOKEN = token
        self.cmd = {"stat": "getMe", "send": "sendMessage"}
        if proxy:
            ip = proxy['ip']
            port = proxy['port']
            user = proxy['user']
            passwd = proxy['password']
            pp = telegram.utils.request.Request(proxy_url='socks5://%s:%s' % (
                ip, port), urllib3_proxy_kwargs={'username': user, 'password': passwd})
        else:
            pp = telegram.utils.request.Request()
        self.bot = telegram.Bot(token=self.BOT_TOKEN, request=pp)

    def stat(self):
        # cmd=self.cmd["stat"]
        try:
            pass
        except Exception as err:
            messToSyslog = "Fail to read telegram_bot status: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)

    def send(self, chat, mess):
        # cmd = self.cmd["send"]
        mess = mess.encode('utf-8')
        try:
            self.bot.sendMessage(chat, mess)
            return True
        except Exception as err:
            messToSyslog = "Fail to sendmessage via telegram_bot: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)


class Handler:
    def __init__(self, queue):
        self.queue = queue

        if queue == "queue_Tgm_1":
            self.notify = self.telegram
        elif queue == "queue_tlgrm":
            self.notify = self.psevdo_telegram
        else:
            self.notify = self.default

        self.params = {"telegram": {"token": "id:token",
                                    "base_url": "https://api.telegram.org/bot",
                                    'proxy': {
                                        'ip': '0.0.0.0',
                                        'port': 9999, 'user': 'some_user', 'password': 'some_password'}},
                       "to_db": {'url_in': 'some url in'}}

    def start_consume(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_consume(self.callback,
                                  queue=self.queue,
                                  no_ack=False, exclusive=False)
            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            # channel.stop_consuming()
            syslog.syslog("Error while consuming %s queue: %s" %
                          (self.queue, str(exc)))
        connection.close()
        sys.exit(1)

        connection.close()

    def callback(self, ch, method, body):
        if self.notify(body):
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def default(self, body):
        messToSyslog = "got " + body + " but not set notifyer"
        syslog.syslog("%s: %s" % (self.queue, messToSyslog))
        return True

    def telegram(self, body):
        syslog.syslog("%s: send data to telegramm %s" % (self.queue, body))
        params = self.params["telegram"]
        t = TelegramAPI(params["token"], proxy=params.get('proxy'))
        data = json.loads(body)
        chat_id = data["chat_id"]
        mess = data["message"]
        return t.send(chat_id, mess) or True

    def psevdo_telegram(self, body):
        params = self.params["to_db"]
        db = CorporateDB(params['url_in'])
        data = json.loads(body)
        res, mess = db.telegram_procedure_exec(
            data['group'], data['message'])
        syslog.syslog("%s: send data for telegramm notification %s with status %s" % (
            self.queue, body, res))
        return True


class CorporateDB:
    def __init__(self, url_in):
        self.connection = dbModule.Connection("login/password")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''BEGIN
                            some_initial_procedure(%s);
                            END;''' % url_in)

    def telegram_procedure_exec(self, group, message):
        self.cursor.execute("""BEGIN
                        another_plsql_procedure(%s);
                        COMMIT;
                        END;""" % message, group=int(group), result_out=result_out, message_out=message_out)
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return result_out.getvalue(), message_out.getvalue()


if __name__ == "__main__":
    syslog.openlog('some_tag', syslog.LOG_PID, syslog.LOG_NOTICE)

    start_consume_one = Consume(CallbackDbOne(), queue='queue_one')
    start_consume_two = Consume(CallbackDbTwo(), queue='queue_two')
    start_consume_three = Consume(CallbackDbThree(), queue='queue_three')
    start_consume_mail = Consume(SendMail('data???').send(), queue='queue_mail')
    start_consume_sms = Consume(SendSMS('data???').send(), queue='queue_sms')
    start_consume_telegram = Consume(SendTelegram('data???').send(), queue='queue_telegram')

    try:
        thr_list = [
            start_consume_one,
            start_consume_two,
            start_consume_three,
            start_consume_mail,
            start_consume_sms,
            start_consume_telegram
        ]

        for n in ["queue_Tgm_1", "queue_tlgrm"]:
            t = Handler(n)
            thr_list.append(t.start_consume)

        Supervisor().start_threads(thr_list)

    except KeyboardInterrupt:
        print("EXIT")
        raise
