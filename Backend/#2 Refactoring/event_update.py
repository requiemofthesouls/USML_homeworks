#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


class EventUpdate:

    def __init__(self, data):
        self.data = data

    def start(self):
        if not self.data:
            return False
        zhost, evid, NumTT = self.data

        server = 'server'
        if zhost == 'server2':
            server = 'server2'

        login = 'event_login'
        password = 'event_password'

        s = requests.Session()
        s.auth = (login, password)

        return True
