#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
import syslog


class Consume:
    def __init__(self, callback, queue=None):
        self.callback = callback
        self.queue = queue

    def start(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )

            channel = connection.channel()
            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_consume(self.callback,
                                  queue='queue_one',
                                  no_ack=False, arguments={"x-priority": 5})

            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            channel.stop_consuming()
            syslog.syslog(f"Error while consuming {self.queue}: {exc}")

        connection.close()
        sys.exit(1)
