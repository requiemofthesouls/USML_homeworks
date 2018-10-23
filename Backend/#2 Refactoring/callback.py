#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .db_process import (
    DBProcessOne,
    DBProcessTwo,
    DBProcessThree,)

from .create import (
    CreateRowOne,
    CreateRowTwo,
    CreateRowThree)

from .event_update import EventUpdate


class CallbackDbOne:
    @staticmethod
    def callback(ch, method, body):
        row = CreateRowOne(body).create()
        db_result = DBProcessOne(row)
        result = EventUpdate(db_result).start()
        if result:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)


class CallbackDbTwo:
    @staticmethod
    def callback(ch, method, body):
        row = CreateRowTwo(body).create()
        db_result = DBProcessTwo(row)
        result = EventUpdate(db_result).start()
        if result:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)


class CallbackDbThree:
    @staticmethod
    def callback(ch, method, body):
        row = CreateRowThree(body).create()
        db_result = DBProcessThree(row)
        result = EventUpdate(db_result).start()
        if result:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)
