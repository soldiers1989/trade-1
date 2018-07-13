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


class _Model:
    def __init__(self, db):
        """
            init model with database connection
        :param db:
        """
        self._db = db

    def tables(self, *args):
        """

        :return:
        """
        return self

    def insert(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self

    def select(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        return self

    def update(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self

    def delete(self):
        """

        :return:
        """
        return self

    def where(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self

    def orderby(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self

    def groupby(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self

    def execute(self):
        """

        :return:
        """
        return self

    def commit(self):
        """

        :return:
        """
        pass

def use(db):
    return _Model(db)

a = _Model(1)

a.tables(

).select(

).where(

)
