"""
    validator
"""
import decimal, re


class ErrorValidation(Exception):
    def __init__(self, err):
        super().__init__(err)


class Validator:
    def __init__(self, **kwargs):
        self._null = kwargs.get('null', False)

    def valid(self, val):
        # check null able
        if not self._null and val is None:
            raise ErrorValidation('value must be not none, current: none')
        return val


class EnumValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._choices = kwargs.get('choices', None)

    def valid(self, val):
        val = super().valid(val)
        if self._choices is not None and not val in self._choices:
            raise ErrorValidation('enum value %s is not in choices: %s' % (str(val), str(self._choices)))
        return val


class IntegerValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)
        if val is None:
            return val

        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorValidation('integer value must be not less than %d, current: %d' % (self._min_value, val))
        if self._max_value is not None and val > self._max_value:
            raise ErrorValidation('integer value must be not more than %d, current: %d' % (self._max_value, val))

        return val


class StringValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        length = kwargs.get('length')
        self._min_length = kwargs.get('min_length', length)
        self._max_length = kwargs.get('max_length', length)

        self._pattern = kwargs.get('pattern', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)
        if val is None:
            return val

        length = len(val)
        # check string length
        if self._min_length is not None and length < self._min_length:
            raise ErrorValidation('string length must be not less than %d, current: %d' % (self._min_length, length))
        if self._max_length is not None and length > self._max_length:
            raise ErrorValidation('string length must be not more than %d, current: %d' % (self._max_length, length))

        # check string pattern
        if self._pattern is not None and re.match(self._pattern, val) is None:
            raise ErrorValidation('string pattern not match: %s, current: %s' % (self._pattern, val))

        return val


class FloatValidator(Validator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._min_value = kwargs.get('min_value', None)
        self._max_value = kwargs.get('max_value', None)

    def valid(self, val):
        # super valid
        val = super().valid(val)
        if val is None:
            return val


        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorValidation('float value must be not less than %d, current: %d' % (self._min_value, val))
        if self._max_value is not None and val > self._max_value:
            raise ErrorValidation('float value must be not more than %d, current: %d' % (self._max_value, val))

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
        if val is None:
            return val

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
            raise ErrorValidation('decimal max digits must be not more than %s, current: %s' % (str(self._digits), str(digits)))

        if self._decimals is not None and decimals > self._decimals:
            raise ErrorValidation('decimal max decimals must be not more than %s, current: %s' % (str(self._decimals), str(decimals)))

        if (self._digits is not None and self._decimals is not None and integers > (self._digits - self._decimals)):
            raise ErrorValidation('decimal max integers must be not more than %s, current: %s' % (str((self._digits - self._decimals)), str(integers)))

        # check value range
        if self._min_value is not None and val < self._min_value:
            raise ErrorValidation('decimal value must be not less than %s, current: %s' % (str(self._min_value), str(val)))

        if self._max_value is not None and val > self._max_value:
            raise ErrorValidation('decimal value must be not more than %s, current: %s' % (str(self._max_value), str(val)))

        return val
