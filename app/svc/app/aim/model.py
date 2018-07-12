"""
    pub model base class
"""


class Model:
    def __init__(self, db):
        """
            init model
        """
        self._db = db

    def begin(self):
        """
            begin transaction
        :return:
        """
        self._db.begin()

    def commit(self):
        """
            commit changes
        :return:
        """
        self._db.commit()

    def execute(self, sql, args=None):
        """
            execute
        :param query:
        :param args:
        :return:
        """
        self._db.execute(sql, args)

    def insert(self, sql, args=None):
        """
            execute
        :param query:
        :param args:
        :return:
        """
        n = self._db.execute(sql, args)
        self._db.commit()
        return n

    def update(self, sql, args=None):
        """
            execute
        :param query:
        :param args:
        :return:
        """
        n = self._db.execute(sql, args)
        self._db.commit()
        return n

    def select(self, sql, args=None):
        """
            select
        :param query:
        :param args:
        :return:
        """
        return self._db.select(sql, args)
