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

        # cursor object
        self._cursor = None

    def connect(self):
        """
            connect to database
        :param config:
        :return:
        """
        if self._conn is None or self._cursor is None:
            self._conn = pymysql.connect(**self._cfg)
            self._cursor = self._conn.cursor()

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
        if self._conn is None:
            return

        self._conn.commit()

    def select(self, sql, args=None):
        """

        :param sql:
        :return:
        """
        # connect to database
        self.connect()

        # excute select query
        self._cursor.execute(sql, args)

        # fetch all results
        results = self._cursor.fetchall()

        return results

    def execute(self, sql, args=None):
        """

        :param sql:
        :param args:
        :return:
        """
        # execute sql
        return self._cursor.execute(sql, args)

    def close(self):
        """
            close connection to database
        :return:
        """
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

        if self._conn is not None:
            self._conn.close()
            self._conn = None
