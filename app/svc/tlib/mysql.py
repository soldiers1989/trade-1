"""
    mysql class
"""
import pymysql


class DBMysql:
    def __init__(self, cfg):
        """
            init mysql db with configure

        """
        # database configure
        self._cfg = cfg

        # database object
        self._conn = None

    def connect(self):
        """
            connect to database
        :param config:
        :return:
        """
        if self._conn is None:
            self._conn = pymysql.connect(**self._cfg, cursorclass = pymysql.cursors.DictCursor)

    def begin(self):
        """
            begin transaction
        :return:
        """
        self.connect()
        self._conn.begin()

    def commit(self):
        """
            commit changes to database
        :return:
        """
        if self._conn is not None:
            self._conn.commit()

    def rollback(self):
        """
            rollback transaction
        :return:
        """
        if self._conn is not None:
            self._conn.rollback()

    def select(self, sql, args=None):
        """

        :param sql:
        :return:
        """
        # connect to database
        self.connect()

        # create cursor
        cursor = self._conn.cursor()

        # execute select query
        cursor.execute(sql, args)

        # fetch all results
        results = cursor.fetchall()

        return results

    def execute(self, sql, args=None):
        """

        :param sql:
        :param args:
        :return:
        """
        # connect to database
        self.connect()

        # create cursor
        cursor = self._conn.cursor()

        # execute sql
        results = cursor.execute(sql, args)

        return results

    def last_row_id(self):
        """
            get last insert primary key id
        :return:
        """
        return self._conn.insert_id()

    def close(self):
        """
            close connection to database
        :return:
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None
