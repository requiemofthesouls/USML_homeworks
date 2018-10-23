#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
import syslog
import re


class DBProcess:
    def __init__(self, row):
        self.connection = None
        self.row = row

    def db_connection(self):
        try:
            self.connection = dbModule.Connection("db_login/db_pass")
        except dbModule.DatabaseError as exc:
            syslog.syslog("DB connection error: %s" % exc)
            return False

    @abstractmethod
    def start(self):
        pass


class DBProcessOne(DBProcess):
    def start(self):
        if not self.row:
            return False
        zhost = self.row[7]
        connection = self.db_connection()

        try:
            cursor = connection.cursor()
            statTT = cursor.var(dbModule.STRING, 255)
            result = cursor.var(dbModule.NUMBER, 255)
            numTT = cursor.var(dbModule.NUMBER, 255)
            cursor.prepare("""BEGIN;
                    procedure_one(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);
                ); END;""")
            self.row.append(result)
            self.row.append(numTT)
            self.row.append(statTT)
            cursor.execute(None, self.row)
            connection.commit()
            cursor.close()
            syslog.syslog("Insert data to db: %s" % self.row[0])
        except Exception as exc:
            syslog.syslog("Error while inserting to db: %s" % exc)
            return False

        event_num = re.search("\s*([0-9]+)", self.row[6]).group(1)
        resultTT = (int(self.row[-3].getvalue()),
                    int(self.row[-2].getvalue()), str(self.row[-1].getvalue()))

        syslog.syslog("Prepare ack one: %s" % self.row)
        return (zhost, event_num, resultTT)


class DBProcessTwo(DBProcess):
    def start(self):
        if not self.row:
            return False
        zhost = self.row[7]
        connection = self.db_connection()

        try:
            cursor = connection.cursor()
            statTT = cursor.var(dbModule.STRING, 255)
            result = cursor.var(dbModule.NUMBER, 255)
            numTT = cursor.var(dbModule.NUMBER, 255)
            cursor.prepare("""BEGIN
            procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);
            END;""")
            self.row.append(result)
            self.row.append(numTT)
            self.row.append(statTT)
            cursor.execute(None, self.row)
            connection.commit()
            cursor.close()
            syslog.syslog("Insert data to db: %s" % self.row[0])
        except Exception as exc:
            syslog.syslog("Error while inserting to db: %s" % exc)
            return False

        syslog.syslog(str(self.row))
        event_num = re.search("\s*([0-9]+)", self.row[3]).group(1)
        event_reg_num = self.row[-2].getvalue()
        if event_reg_num == None:
            event_reg_num = 0
        event_reg_status = str(self.row[-1].getvalue())
        resultTT = (int(event_reg_num), event_reg_status)
        syslog.syslog("Prepare ack two: %s" % self.row)
        return (zhost, event_num, resultTT)


class DBProcessThree(DBProcess):
    def start(self):
        if not self.row:
            return False
        connection = self.db_connection()

        try:
            cursor = connection.cursor()
            cursor.prepare("""BEGIN;
                procedure_three(:1, :2, :3);
                END;""")
            cursor.execute(None, self.row)
            connection.commit()
            syslog.syslog("Insert data to db: %s" % self.row[0])
        except Exception as exc:
            syslog.syslog("Error while inserting to db: %s" % exc)
            return False

        return True
