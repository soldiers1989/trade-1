"""
    message template
"""


# short message template object
class _Sms:
    def __init__(self, tpl, expires):
        self._tpl = tpl
        self._expires = expires



sms = {
    'pv': '[abc] %s xxx验证码，2分钟内有效', # phone verify
}