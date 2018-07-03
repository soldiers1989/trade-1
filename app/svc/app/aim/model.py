"""
    pub model base class
"""


class Model:
    def __init__(self, db):
        """
            init model
        """
        self._db = db


    def execute(self, sql, args=None):
        """
            execute
        :param query:
        :param args:
        :return:
        """
        return self._db.execute(sql, args)

    def select(self, sql, args=None):
        """
            select
        :param query:
        :param args:
        :return:
        """
        return self._db.select(sql, args)
