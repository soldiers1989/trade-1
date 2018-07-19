"""
    message template
"""
_platform = 'abc'

# short message template object
class _Sms:
    def __init__(self, tpl, expires, platform=_platform):
        self._tpl = tpl
        self._expires = expires
        self._platform = platform

    def format(self, code):
        """
            format message
        :param code:
        :return:
        """
        return self._platform+self._tpl % code


# template messages
sms = {
    'general': _Sms('%s, 您的验证码，2分钟内有效', 120), # general sms template
}
