"""
    sql generator
"""


class SQLError(Exception):
    """
        sql helper error
    """
    def __init__(self, msg):
        self._msg = msg

    @property
    def msg(self):
        return self._msg

    def __str__(self):
        return self._msg


class _Select:
    """
        select sql
    """
    def __init__(self):
        self._tables = None
        self._columns = None
        self._wheres = None
        self._orderby = None
        self._order = None
        self._groupby = None

    def columns(self, *cols):
        """

        :param cols: array|tupple, columns
        :return:
        """
        self._columns = cols
        return self

    def tables(self, *tbls):
        """

        :param tbls:
        :return:
        """
        self._tables = tbls
        return self

    def where(self, **conds):
        """

        :param conds:
        :return:
        """
        if self._wheres is None:
            self._wheres = []

        if len(conds) > 0:
            self._wheres.append(conds)
        return self

    def orderby(self, *cols):
        """

        :param cols:
        :return:
        """
        self._orderby = cols
        return self

    def groupby(self, *cols):
        """

        :param cols:
        :return:
        """
        self._groupby = cols
        return self

    def asc(self):
        """

        :return:
        """
        self._order = 'asc'
        return self

    def desc(self):
        """

        :return:
        """
        self._order = 'desc'
        return self

    def sql(self):
        """

        :return:
        """
        # sql string
        s = ''

        # select clause
        if self._columns is None:
            raise SQLError('查询语句没有指定列')
        s = s + 'select ' + '`' + '`,`'.join(self._columns) + '` '

        # from clause
        if self._tables is None:
            raise SQLError('查询语句没有指定表')
        s = s + 'from ' + '`' + '`,`'.join(self._tables) + '` '

        # where clause
        if self._wheres is not None:
            wheres = []
            for where in self._wheres:
               wheres.append('`'+ '`=%s and `'.join(where.keys()) + '`=%s ')

            if len(wheres) > 0:
                s = s + 'where ' + 'or '.join(wheres)

        # group by clause
        if self._groupby is not None:
            s = s + 'group by ' + '`' + '`, `'.join(self._groupby) + '` '

        # order by clause
        if self._orderby is not None:
            s = s + 'order by ' +'`' + '`, `'.join(self._orderby) + '` '

        # order clause
        if self._order is not None:
            s = s + self._order

        return s

    def args(self):
        """

        :return:
        """
        vals = []
        for where in self._wheres:
            vals.extend(where.values())
        return tuple(vals)


select = _Select


class _Insert:
    """
        insert sql helper
    """
    def __init__(self):
        self._table = None
        self._columns = None
        self._values = None

    def colvals(self, **cvals):
        """

        :param cvals:
        :return:
        """
        self._columns = list(cvals.keys())
        self._values = list(cvals.values())
        return self

    def columns(self, *cols):
        """

        :param cols: array|tupple, columns
        :return:
        """
        self._columns = cols
        return self

    def table(self, tbl):
        """

        :param tbl:
        :return:
        """
        self._table = tbl
        return self

    def values(self, *vals):
        """

        :param conds:
        :return:
        """
        self._values = vals
        return self

    def sql(self):
        """

        :return:
        """
        # sql string
        s = ''

        # table clause #
        if self._table is None:
            raise SQLError('插入语句没有指定表')
        s = s + 'insert into `' + self._table + '` '

        # columns clause #
        if self._columns is None:
            raise SQLError('插入语句没有指定列')
        s = s + '(' + '`' + '`,`'.join(self._columns) + '`) '

        # values clause #
        if self._values is None:
            raise SQLError('插入语句没有指定值')

        # check items
        if len(self._columns) != len(self._values):
            raise SQLError('插入语句列和值不对应')

        # add ? clause
        v = []
        for i in range(len(self._columns)):
            v.append('%s')
        s = s + 'values (' + ','.join(v) + ')'

        return s

    def args(self):
        """

        :return:
        """
        return self._values


insert = _Insert


class _Update:
    """
        update sql
    """
    def __init__(self):
        self._table = None
        self._cvals = None
        self._wheres = None

    def set(self, **cvals):
        """

        :param cols: array|tupple, columns
        :return:
        """
        self._cvals = cvals
        return self

    def table(self, tbl):
        """

        :param tbls:
        :return:
        """
        self._table = tbl
        return self

    def where(self, **conds):
        """

        :param conds:
        :return:
        """
        if self._wheres is None:
            self._wheres = []

        if len(conds) > 0:
            self._wheres.append(conds)

        return self

    def sql(self):
        """

        :return:
        """
        # sql string
        s = ''

        # update clause
        if self._table is None:
            raise SQLError('更新语句没有指定表')
        s = s + 'update ' + '`' + self._table + '` '

        # set clause
        if self._cvals is None:
            raise SQLError('更新语句没有指定值')
        s = s + 'set `' + '`=%s, `'.join(self._cvals.keys()) + '`=%s '

        # where clause
        if self._wheres is not None:
            wheres = []
            for where in self._wheres:
               wheres.append('`'+ '`=%s and `'.join(where.keys()) + '`=%s ')

            if len(wheres) > 0:
                s = s + 'where ' + 'or '.join(wheres)

        return s

    def args(self):
        """

        :return:
        """
        vals = []

        # value args
        vals.extend(self._cvals.values())

        # where args
        for where in self._wheres:
            vals.extend(where.values())

        return tuple(vals)


update = _Update


class _Delete:
    """
        delete sql
    """
    def __init__(self):
        self._table = None
        self._wheres = None

    def table(self, tbl):
        """

        :param tbls:
        :return:
        """
        self._table = tbl
        return self

    def where(self, **conds):
        """

        :param conds:
        :return:
        """
        if self._wheres is None:
            self._wheres = []

        if len(conds) > 0:
            self._wheres.append(conds)

        return self

    def sql(self):
        """

        :return:
        """
        # sql string
        s = ''

        # delete clause
        if self._table is None:
            raise SQLError('更新语句没有指定表')
        s = s + 'delete from ' + '`' + self._table + '` '

        # where clause
        if self._wheres is not None:
            wheres = []
            for where in self._wheres:
               wheres.append('`'+ '`=%s, and `'.join(where.keys()) + '`=%s ')

            if len(wheres) > 0:
                s = s + 'where ' + 'or '.join(wheres)

        return s

    def args(self):
        """

        :return:
        """
        vals = []

        # where args
        for where in self._wheres:
            vals.extend(where.values())

        return tuple(vals)


delete = _Delete


class _Util:
    @staticmethod
    def repeat(s, cnt, sep):
        """
            repeat string by @s for @cnt times with separator @sep
        :param s:
        :param cnt:
        :param sep:
        :return:
        """
        v = []
        for i in range(0, cnt):
            v.append(s)
        return sep.join(v)


util = _Util


if __name__ == '__main__':
    s = select().columns('a', 'b').tables('tb1', 'tb2').where(a=1, b='x').where(a='c').orderby('a').desc()
    print(s.sql())
    print(s.args())

    s = insert().columns('a', 'b').table('tb1').values(1, 'a')
    print(s.sql())
    print(s.args())

    s = update().table('tb1').set(a=1, b='b').where(c=0).where(c=1)
    print(s.sql())
    print(s.args())

    s = delete().table('tb1').where(a=1, b=2).where(a=3, b=4)
    print(s.sql())
    print(s.args())

    print(util.repeat('?', 10, ','))
