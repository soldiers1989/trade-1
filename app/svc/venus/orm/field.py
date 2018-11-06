"""
    field types
"""
import datetime
import decimal

from . import validator


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


class Field:
    def __init__(self, validatorcls, **kwargs):
        """
            init field
        :param code:
        :param name:
        """
        self.validator = validatorcls(**kwargs)

        self.code = None
        self.name = kwargs.get('name')

        self.default = self._value(kwargs.get('default'))

    def _value(self, val):
        """
            convert value
        :param val:
        :return:
        """
        return val

    def valid(self, val):
        """
            valid value
        :param val:
        :return:
        """
        return self.validator.valid(val)

    def value(self, val):
        """
            convert and valid input value
        :param val:
        :return:
        """
        try:
            return self.valid(self._value(val))
        except validator.ErrorValidation as e:
            raise ErrorFieldValue('%s: %s' % (str(self.code), str(e)))


class EnumField(Field):
    def __init__(self, **kwargs):
        super().__init__(validator.EnumValidator, **kwargs)

    def _value(self, val):
        return str(val)


class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__(validator.Validator, **kwargs)

    def _value(self, val):
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
    def __init__(self, **kwargs):
        super().__init__(validator.IntegerValidator, **kwargs)

    def _value(self, val):
        if val is None:
            return None
        try:
            return int(val)
        except:
            raise ErrorFieldValue('invalid integer value %s' % str(val))


class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__(validator.FloatValidator, **kwargs)

    def _value(self, val):
        if val is None:
            return None
        try:
            return float(val)
        except:
            raise ErrorFieldValue('invalid float value %s' % str(val))


class DecimalField(Field):
    def __init__(self, **kwargs):
        super().__init__(validator.DecimalValidator, **kwargs)
        self._digits = kwargs.get('digits', None)

    @property
    def context(self):
        return decimal.Context(prec=self._digits)

    def _value(self, val):
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
    def __init__(self, **kwargs):
        super().__init__(validator.StringValidator, **kwargs)

    def _value(self, val):
        if val is None:
            return None
        try:
            return str(val)
        except:
            raise ErrorFieldValue('invalid string value %s' % str(val))


class TimeField(Field):
    def __init__(self, **kwargs):
        super().__init__(validator.Validator, **kwargs)
        self.format = kwargs.get('format', '%H:%M:%S')

    def _value(self, val):
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
    def __init__(self, **kwargs):
        super().__init__(validator.Validator, **kwargs)
        self.format = kwargs.get('format', '%Y-%m-%d')

    def _value(self, val):
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
    def __init__(self, **kwargs):
        super().__init__(validator.Validator, **kwargs)
        self.format = kwargs.get('format', '%Y-%m-%d %H:%M:%S')

    def _value(self, val):
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
