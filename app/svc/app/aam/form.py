"""
    form base class
"""


class _FormError(Exception):
    """
        form exception
    """
    def __init__(self, msg):
        super.__init__(self, msg)


class Form:
    """
        form base class
    """
    def __init__(self):
        pass

    def validate(self):
        pass


def error(msg="表单数据错误"):
    """
        create a form error object
    :param msg:
    :return:
    """
    return _FormError(msg)


def number(obj, min=None, max=None):
    """
        check if obj if number data
    :param obj:
    :param min:
    :param max:
    :return:
    """
    pass