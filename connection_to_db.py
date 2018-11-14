#-*- coding: utf-8 -*-

import sqlite3


class ConnectionToDB():

        def __init__(self, db_name):
            self.connection = None
            self.cursor = None
            self.db = db_name

        def get_connect(self):
            self.connection = sqlite3.connect(self.db)
            return self.connection

        def get_cursor(self):
            return self.get_connect().cursor()

        def close_connection(self):
            pass
