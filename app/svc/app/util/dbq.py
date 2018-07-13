"""
    database access
"""


class Dbq:
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
