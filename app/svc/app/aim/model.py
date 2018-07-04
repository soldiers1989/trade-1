"""
    pub model base class
"""


class Model:
    def __init__(self, db):
        """
            init model
        """
        self._db = db

    def _begin(self):
        """
            begin transaction
        :return:
        """
        self._db.begin()

    def _commit(self):
        """
            commit changes
        :return:
        """
        self._db.commit()

    def _execute(self, sql, args=None):
        """
            execute
        :param query:
        :param args:
        :return:
        """
        return self._db.execute(sql, args)

    def _select(self, sql, args=None):
        """
            select
        :param query:
        :param args:
        :return:
        """
        return self._db.select(sql, args)
