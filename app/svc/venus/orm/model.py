"""
    pub model base class
"""
from . import field, query


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        #get declared fields
        fields = {}
        for code, f in attrs.items():
            if issubclass(f.__class__, field.Field):
                f.code = code
                if f.name is None:
                    f.name = code
                fields[code] = f

        # remove declare in attrs
        for k in fields.keys():
            del attrs[k]

        # table name
        attrs['__table__'] = attrs.get('__table__', name)
        # model fields
        attrs['__fields__'] = fields

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=MetaModel):
    def __init__(self, **kwargs):
        super().__init__()
        for code, field in self.fields().items():
            self[code] = field.value(kwargs.get(code, field.default))

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        field = self.fields().get(name)
        if field is None:
            raise field.ErrorFieldNotExist(name)

        self[name] = field.value(value)

    def values(self):
        """
            object values
        :return:
            list
        """
        vals = []
        for name in self.fieldnames():
            vals.append(self[name])
        return vals

    @classmethod
    def fields(cls):
        """
            get table fields
        :return:
            dict, name->field
        """
        return cls.__fields__

    @classmethod
    def tablename(cls):
        return cls.__table__

    @classmethod
    def fieldcodes(cls):
        """
            get table fields code
        :return:
            list
        """
        return list(cls.__fields__.keys())

    @classmethod
    def fieldnames(cls):
        """
            get table fields name
        :return:
            list
        """
        names = []
        for field in cls.__fields__.values():
            names.append(field.name)
        return names

    @classmethod
    def filter(cls, db, *q, **filters):
        """
            use specified database for query
        :param db: obj, database object
        :param q: obj, query.Q object
        :param filters: dict, filter conditions
        :return:
            query set object
        """
        return query.QuerySet(db, cls, *q, **filters)

    def save(self, db):
        """
            save current object to specified db
        :return:
        """
        return query.QuerySet(db, self.__class__).insert(self)
