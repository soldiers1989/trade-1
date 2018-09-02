"""
    pub model base class
"""
import decimal, datetime


class ErrorFieldNotExist(Exception):
    def __init__(self, err):
        super().__init__(err)


class ErrorFieldNotSpecified(Exception):
    def __init__(self, err = 'unknown field type'):
        super().__init__(err)

class ErrorFieldValue(Exception):
    def __init__(self, err):
        super().__init__(err)


class ErrorFieldType(Exception):
    def __init__(self, err):
        super().__init__(err)


class Validator:
    def __init__(self, **kwargs):
        self._null = kwargs.get('null', False)

    def valid(self, val):
        # check null able
        if val is None:
            if not self._null:
                raise ErrorFieldValue('value must be not null, current: None')
            return None
        return val


class IntegerValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)

        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorFieldValue('integer value must be not less than %d, current: %d' % (self._min_value, val))
        if self._max_value is not None and val > self._max_value:
            raise ErrorFieldValue('integer value must be not more than %d, current: %d' % (self._max_value, val))

        return val


class StringValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_length = kwargs.get('min_length', None)
        self._max_length = kwargs.get('max_length', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)

        length = len(val)
        # check string length
        if self._min_length is not None and length < self._min_length:
            raise ErrorFieldValue('string length must be not less than %d, current: %d' % (self._min_length, length))
        if self._max_length is not None and length > self._max_length:
            raise ErrorFieldValue('string length must be not more than %d, current: %d' % (self._max_length, length))

        return val


class FloatValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)

        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorFieldValue('float value must be not less than %d, current: %d' % (self._min_value, val))
        if self._max_value is not None and val > self._max_value:
            raise ErrorFieldValue('float value must be not more than %d, current: %d' % (self._max_value, val))

        return val


class DecimalValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._digits = kwargs.get('digits', None)
        self._decimals = kwargs.get('decimals', None)

        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

        self._min_value = decimal.Decimal(self._min_value) if self._min_value is not None else None
        self._max_value = decimal.Decimal(self._max_value) if self._max_value is not None else None

    def valid(self, val):
        # super valid
        val = super().valid(val)

        # get value's digits and decimals length
        digit_tuple, exponent = val.as_tuple()[1:]
        if exponent >= 0:
            digits = len(digit_tuple) + exponent
            decimals = 0
        else:
            if abs(exponent) > len(digit_tuple):
                digits = decimals = abs(exponent)
            else:
                digits = len(digit_tuple)
                decimals = abs(exponent)
        integers = digits - decimals

        # check value format
        if self._digits is not None and digits > self._digits:
            raise ErrorFieldValue('decimal max digits must be not more than %s, current: %s' % (str(self._digits), str(digits)))

        if self._decimals is not None and decimals > self._decimals:
            raise ErrorFieldValue('decimal max decimals must be not more than %s, current: %s' % (str(self._decimals), str(decimals)))

        if (self._digits is not None and self._decimals is not None and integers > (self._digits - self._decimals)):
            raise ErrorFieldValue('decimal max integers must be not more than %s, current: %s' % (str((self._digits - self._decimals)), str(integers)))

        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorFieldValue('decimal value must be not less than %s, current: %s' % (str(self._min_value), str(val)))

        if self._max_value is not None and val > self._max_value:
            raise ErrorFieldValue('decimal value must be not more than %s, current: %s' % (str(self._max_value), str(val)))

        return val


class Field:
    def __init__(self, name, **kwargs):
        """
            init field
        :param code:
        :param name:
        """
        self.code = None
        self.name = name

        default = kwargs.get('default')
        self.default = None if default is None else self.valueof(default)

    def value(self, val):
        """
            convert value
        :param val:
        :return:
        """
        raise ErrorFieldNotSpecified()

    def valid(self, val):
        """
            valid value
        :param val:
        :return:
        """
        return self.validator.valid(val)

    def valueof(self, val):
        """
            convert and valid input value
        :param val:
        :return:
        """
        return self.valid(self.value(val))


class EnumField(Field):
    def __init__(self, name, **kwargs):
        self.validator = Validator(**kwargs)

        self.choices = kwargs.get('choices')
        if self.choices is None or len(self.choices) < 1:
            raise ErrorFieldType('invalid enum field choices, must be more than 0')

        cls = None
        for chioce in self.choices:
            if cls is None:
                cls = chioce.__class__
            else:
                if cls != chioce.__class__:
                    raise ErrorFieldType('invalid enum field choices, must be save type')

        self.typecls = kwargs.get('typecls')
        if self.typecls is None:
            self.typecls = self.choices[0].__class__
        else:
            if self.typecls != self.choices[0].__class__:
                raise ErrorFieldType('invalid enum field choices, conflict with typecls')

        super().__init__(name, **kwargs)

    def value(self, val):
        try:
            val = self.typecls(val)
            return val
        except:
            raise ErrorFieldValue('value %s is not valid enum type' % (val.__class__.__name__))

    def valid(self, val):
        return val in self.choices


class BooleanField(Field):
    def __init__(self, name, **kwargs):
        self.validator = Validator(**kwargs)
        super().__init__(name, **kwargs)

    def value(self, val):
        if val in (True, False):
            return val
        if val is None or val in ('None',):
            return None
        if val in ('1', 'True', 'true'):
            return True
        if val in ('0', 'False', 'false'):
            return False
        raise ErrorFieldValue('invalid boolean value %s' % str(val))


class IntegerField(Field):
    def __init__(self, name, **kwargs):
        self.validator = IntegerValidator(**kwargs)
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return None
        try:
            return int(val)
        except:
            raise ErrorFieldValue('invalid integer value %s' % str(val))


class FloatField(Field):
    def __init__(self, name, **kwargs):
        self.validator = FloatValidator(**kwargs)
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return None
        try:
            return float(val)
        except:
            raise ErrorFieldValue('invalid float value %s' % str(val))


class DecimalField(Field):
    def __init__(self, name, **kwargs):
        self.validator = DecimalValidator(**kwargs)
        self._digits = kwargs.get('digits', None)
        super().__init__(name, **kwargs)

    @property
    def context(self):
        return decimal.Context(prec=self._digits)

    def value(self, val):
        if val is None:
            return None

        try:
            if isinstance(val, float):
                return self.context.create_decimal_from_float(val)
            else:
                return decimal.Decimal(val)
        except:
            raise ErrorFieldValue('invalid decimal value %s' % str(val))


class StringField(Field):
    def __init__(self, name, **kwargs):
        self.validator = StringValidator(**kwargs)
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return None
        try:
            return str(val)
        except:
            raise ErrorFieldValue('invalid string value %s' % str(val))


class TimeField(Field):
    def __init__(self, name, **kwargs):
        self.validator = Validator(**kwargs)
        self.format = kwargs.get('format', '%H:%M:%S')
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return val
        if isinstance(val, datetime.time):
            return val
        if isinstance(val, datetime.datetime):
            return val.time()

        try:
            return datetime.datetime.strptime(str(val), self.format).time()
        except:
            raise ErrorFieldValue('invalid date value %s' % (str(val)))


class DateField(Field):
    def __init__(self, name, **kwargs):
        self.validator = Validator(**kwargs)
        self.format = kwargs.get('format', '%Y-%m-%d')
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return val
        if isinstance(val, datetime.date):
            return val
        if isinstance(val, datetime.datetime):
            return val.date()

        try:
            return datetime.datetime.strptime(str(val), self.format).date()
        except:
            raise ErrorFieldValue('invalid date value %s' % (str(val)))


class DateTimeField(Field):
    def __init__(self, name, **kwargs):
        self.validator = Validator(**kwargs)
        self.format = kwargs.get('format', '%Y-%m-%d %H:%M:%S')
        super().__init__(name, **kwargs)

    def value(self, val):
        if val is None:
            return val
        if isinstance(val, datetime.datetime):
            return val
        if isinstance(val, datetime.date):
            return datetime.datetime(val.year, val.month, val.day)

        try:
            return datetime.datetime.strptime(str(val), self.format)
        except:
            raise ErrorFieldValue('invalid date time value %s' % (str(val)))


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        #get declared fields
        fields = {}
        for code, field in attrs.items():
            if issubclass(field.__class__, Field):
                fields[code] = field

        # remove declare in attrs
        for k in fields.keys():
            del attrs[k]

        # save fields
        attrs['__fields__'] = fields

        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=MetaModel):
    def __init__(self, **kwargs):
        for code, field in self.__fields__.items():
            self[code] = field.valueof(kwargs.get(code, field.default))

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        field = self.__fields__.get(name)
        if field is None:
            raise ErrorFieldNotExist(name)

        self[name] = field.valueof(value)


class TestModel(Model):
    id = IntegerField('ID', min_value=2)
    name = StringField('名称', null=True)


if __name__ == '__main__':
    a = TestModel(id=2, name='abc', age=12)
    a.id = 3
    print(a)
