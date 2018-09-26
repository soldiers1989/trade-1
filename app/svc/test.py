#from lib.stock.quote.daily import quotes
from tlib.stock.quote.level5 import quotes
import threading, time, copy

class T(threading.Thread):
    id = "abc"
    name = "123"
    def run(self):
        print('hello')


class Stm:
    def __init__(self):
        pass

    def __enter__(self):
        print('enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')

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


class _Cond:
    # operators->sql format templates
    OPERATORS = ('eq', 'lt', 'le', 'gt', 'ge', 'in', 'startswith', 'endswith', 'contains')

    def __init__(self, name, value):
        """
            init cond
        :param lvalue: obj, left value
        :param rvalue: obj, right value
        """
        self._name, self._not, self._operator = _Cond.parse(name)
        self._value = value

    def sql(self):
        """
            sql
        :return:
        """
        if self._operator == 'eq':
            if self._not:
                return 'not `%s`='%(self._name)+'%s'
            else:
                return '`%s`=' % (self._name) + '%s'
        elif self._operator == 'lt':
            if self._not:
                return 'not `%s`<' % (self._name) + '%s'
            else:
                return '`%s`<' % (self._name) + '%s'
        elif self._operator == 'le':
            if self._not:
                return 'not `%s`<=' % (self._name) + '%s'
            else:
                return '`%s`<=' % (self._name) + '%s'
        elif self._operator == 'gt':
            if self._not:
                return 'not `%s`>' % (self._name) + '%s'
            else:
                return '`%s`>' % (self._name) + '%s'
        elif self._operator == 'ge':
            if self._not:
                return 'not `%s`>=' % (self._name) + '%s'
            else:
                return '`%s`>=' % (self._name) + '%s'
        elif self._operator == 'in':
            if isinstance(self._value, list) or isinstance(self._value, tuple):
                nelmts = len(self._value)
            else:
                nelmts = 1

            if self._not:
                return '`%s` not in (%s)' % (self._name, ','.join(['%s' for i in range(0, nelmts)]))
            else:
                return '`%s` in (%s)' % (self._name, ','.join(['%s' for i in range(0, nelmts)]))
        elif self._operator == 'startswith':
            if self._not:
                return '`%s` not like ' % self._name + '%s%%'
            else:
                return '`%s` like ' % self._name + '%s%%'
        elif self._operator == 'endswith':
            if self._not:
                return '`%s` not like %%' % self._name + '%s'
            else:
                return '`%s` like %%' % self._name + '%s'
        elif self._operator == 'contains':
            if self._not:
                return '`%s` not like %%' % self._name + '%s%%'
            else:
                return '`%s` like %%' % self._name + '%s%%'
        else:
            raise SQLError('条件格式错误：%s' % self._operator)

    def args(self):
        if isinstance(self._value, list) or isinstance(self._value, tuple):
            return list(self._value)
        else:
            return [str(self._value)]

    @staticmethod
    def parse(name):
        """
            name format: xxx/xxx<__not>__(eq/lt/le/gt/ge/in/startswith/endswith/contains)
        :param name:
        :return:
            name(str), not(boolean), operator(str)
        """
        # parse name
        items = name.split('__')
        nitems = len(items)

        # check parse results
        if nitems == 0 or nitems > 3:
            raise SQLError('条件格式错误：%s' % name)

        # parse condition
        if nitems == 1:
            return items[0], False, 'eq'
        elif nitems == 2:
            if items[1] not in _Cond.OPERATORS:
                raise SQLError('条件格式错误：%s' % name)
            return items[0], False, items[1]
        elif nitems == 3:
            if items[2] not in _Cond.OPERATORS or items[1] !='not':
                raise SQLError('条件格式错误：%s' % name)
            return items[0], True, items[2]
        else:
            SQLError('条件格式错误：%s' % name)

class _Node:
    """
    A single internal node in the tree graph. A Node should be viewed as a
    connection (the root) with the children being either leaf nodes or other
    Node instances.
    """
    # Standard connector type. Clients usually won't use this at all and
    # subclasses will usually override the value.
    default = 'DEFAULT'

    def __init__(self, children=None, connector=None, negated=False):
        """Construct a new Node. If no connector is given, use the default."""
        self.children = children[:] if children else []
        self.connector = connector or self.default
        self.negated = negated

    # Required because django.db.models.query_utils.Q. Q. __init__() is
    # problematic, but it is a natural Node subclass in all other respects.
    @classmethod
    def _new_instance(cls, children=None, connector=None, negated=False):
        obj = _Node(children, connector, negated)
        obj.__class__ = cls
        return obj

    def __str__(self):
        template = '(NOT (%s: %s))' if self.negated else '(%s: %s)'
        return template % (self.connector, ', '.join(str(c) for c in self.children))

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

    def __deepcopy__(self, memodict):
        obj = _Node(connector=self.connector, negated=self.negated)
        obj.__class__ = self.__class__
        obj.children = copy.deepcopy(self.children, memodict)
        return obj

    def __len__(self):
        """Return the the number of children this node has."""
        return len(self.children)

    def __bool__(self):
        """Return whether or not this node has children."""
        return bool(self.children)

    def __contains__(self, other):
        """Return True if 'other' is a direct child of this instance."""
        return other in self.children

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if (self.connector, self.negated) == (other.connector, other.negated):
            return self.children == other.children
        return False

    def __hash__(self):
        return hash((self.__class__, self.connector, self.negated) + tuple(self.children))

    def add(self, data, conn_type, squash=True):
        if data in self.children:
            return data
        if not squash:
            self.children.append(data)
            return data
        if self.connector == conn_type:
            # We can reuse self.children to append or squash the node other.
            if (isinstance(data, _Node) and not data.negated and
                    (data.connector == conn_type or len(data) == 1)):
                self.children.extend(data.children)
                return self
            else:
                # We could use perhaps additional logic here to see if some
                # children could be used for pushdown here.
                self.children.append(data)
                return data
        else:
            obj = self._new_instance(self.children, self.connector,
                                     self.negated)
            self.connector = conn_type
            self.children = [obj, data]
            return data

    def negate(self):
        """Negate the sense of the root connector."""
        self.negated = not self.negated


class Q(_Node):
    # Connection types
    AND = 'AND'
    OR = 'OR'
    default = AND

    def __init__(self, **kwargs):
        connector = kwargs.pop('_connector', None)
        negated = kwargs.pop('_negated', False)
        super().__init__(children=sorted(kwargs.items()), connector=connector, negated=negated)

    def _combine(self, other, conn):
        if not isinstance(other, Q):
            raise TypeError(other)

        if not other:
            return copy.deepcopy(self)
        elif not self:
            return copy.deepcopy(other)

        obj = type(self)()
        obj.connector = conn
        obj.add(self, conn)
        obj.add(other, conn)
        return obj

    def __or__(self, other):
        return self._combine(other, self.OR)

    def __and__(self, other):
        return self._combine(other, self.AND)

    def __invert__(self):
        obj = type(self)()
        obj.add(self, self.AND)
        obj.negate()
        return obj

    def sql(self):
        """
            generate prepared sql
        :return:
        """
        childs = []
        for child in self.children:
            if isinstance(child, self.__class__):
                template = 'NOT (%s)' if self.negated else '(%s)'
                childs.append(template % child.sql())
            else:
                childs.append(Q.tpl(child[0], child[1]))

        sep = ' NOT %s ' % self.connector if self.negated else ' %s ' % self.connector
        return sep.join(childs)

    def args(self):
        """
            generate prepared args
        :return:
        """
        childs = []
        for child in self.children:
            if isinstance(child, self.__class__):
                childs.extend(child.args())
            else:
                if isinstance(child[1], tuple) or isinstance(child[1], list):
                    childs.extend(child[1])
                else:
                    childs.append(child[1])

        return childs

    @staticmethod
    def tpl(cname, cvalue):
        """
            generate sql template by conditon name
        :return:
        """
        # operation compare definition
        OP_CMP = {
            'eq': '`%s`=%s',
            'lt': '`%s`<%s',
            'le': '`%s`<=%s',
            'gt': '`%s`>%s',
            'ge': '`%s`>=%s',
            'ne': '`%s`!=%s'
        }

        # operation in definition
        OP_IN = {
            'in': '`%s` in (%s)'
        }

        # operation like definition
        OP_LIKE = {
            'startswith': '`%s` like \'%s%%\'',
            'endswith': '`%s` like \'%%%s\'',
            'contains': '`%s` like \'%%%s%%\''
        }

        # parse name
        items = cname.split('__')
        nitems = len(items)

        # check parse results
        if nitems == 0 or nitems > 2:
            raise SQLError('条件格式错误：%s' % cname)

        # parse condition
        if nitems == 1:
            name = items[0]
            return '%s=%s' % (name, '%s')
        elif nitems == 2:
            name, op = items[0], items[1]

            if op in list(OP_CMP.keys()):
                return OP_CMP[op] % (name , '%s')
            elif op in list(OP_IN.keys()):
                # elements of in condition
                nelmts = len(cvalue) if isinstance(cvalue, list) or isinstance(cvalue, tuple) else 1
                return OP_IN[op] % (name, ','.join(['%s' for i in range(0, nelmts)]))
            elif op in list(OP_LIKE.keys()):
                return OP_LIKE[op] % (name, '%s')
            else:
                raise SQLError('条件格式错误：%s' % cname)

        else:
            raise SQLError('条件格式错误：%s' % cname)


if __name__ == "__main__":
    q1 = Q(a_lt='1') | (Q(x=10) & Q(b=2) | Q(c=3))
    print(q1.sql())

    q2 = Q(d__in=4) & Q(e__in=(50,51,52)) & Q(f__in=('6','7'))
    print(q2)

    q3 = Q(g__contains='7') | Q(h__endswith='8') | Q(i__startswith='9')
    print(q3)

    q4 = q1 & q2 | ~q3
    print(q4.sql())
    print(q4.args())
