"""
    pub model base class
"""
from decimal import Decimal


class ErrorFieldNotExist(Exception):
    def __init__(self, err):
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

    def valid(self, value):
        # check null able
        if value is None:
            if not self._null:
                raise ErrorFieldValue('value must be not null, current: None')
            return None
        return value


class IntegerValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, value):
        # super valid
        value = super().valid(value)

        # translate value
        value = int(value)

        # check value range
        if self._min_value is not None and value < self._min_value:
            raise ErrorFieldValue('integer value must be not less than %d, current: %d' % (self._min_value, value))
        if self._max_value is not None and value > self._max_value:
            raise ErrorFieldValue('integer value must be not more than %d, current: %d' % (self._max_value, value))

        return value


class StringValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_length = kwargs.get('min_length', None)
        self._max_length = kwargs.get('max_length', None)

    def valid(self, value):
        # super valid
        value = super().valid(value)

        # translate value
        value = str(value)

        length = len(value)
        # check string length
        if self._min_length is not None and length < self._min_length:
            raise ErrorFieldValue('string length must be not less than %d, current: %d' % (self._min_length, length))
        if self._max_length is not None and length > self._max_length:
            raise ErrorFieldValue('string length must be not more than %d, current: %d' % (self._max_length, length))

        return value


class FloatValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, value):
        # super valid
        value = super().valid(value)

        # translate value
        value = float(value)

        # check value range
        if self._min_value is not None and value < self._min_value:
            raise ErrorFieldValue('float value must be not less than %d, current: %d' % (self._min_value, value))
        if self._max_value is not None and value > self._max_value:
            raise ErrorFieldValue('float value must be not more than %d, current: %d' % (self._max_value, value))

        return value


class DecimalValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._digits = kwargs.get('digits', None)
        self._decimals = kwargs.get('decimals', None)

        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

        self._min_value = Decimal(self._min_value) if self._min_value is not None else None
        self._max_value = Decimal(self._max_value) if self._max_value is not None else None

    def valid(self, value):
        # super valid
        value = super().valid(value)

        # translate value
        value = Decimal(str(value))

        # get value's digits and decimals length
        digit_tuple, exponent = value.as_tuple()[1:]
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
        if self._min_value is not None and value < self._min_value:
            raise ErrorFieldValue('decimal value must be not less than %s, current: %s' % (str(self._min_value), str(value)))

        if self._max_value is not None and value > self._max_value:
            raise ErrorFieldValue('decimal value must be not more than %s, current: %s' % (str(self._max_value), str(value)))

        return value


class Field:
    def __init__(self, name, **kwargs):
        """
            init field
        :param code:
        :param name:
        """
        self.code = None
        self.name = name
        self.default = kwargs.get('default', None)
        self.validator = Validator()

    def valid(self, val):
        """
            valid value
        :param val:
        :return:
        """
        return self.validator.valid(val)


class IntegerField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.validator = IntegerValidator(**kwargs)


class FloatField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class DecimalField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class StringField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class DateField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


class EnumField(Field):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)


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
            self[code] = field.valid(kwargs.get(code, field.default))

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        field = self.__fields__.get(name)
        if field is None:
            raise ErrorFieldNotExist(name)

        self[name] = field.valid(value)


class TestModel(Model):
    id = IntegerField('ID', min_value=2)
    name = StringField('名称')


if __name__ == '__main__':
    a = TestModel(id=1, name1='abc', age=12)
    a.id = 1
    print(a)
