"""
    generate verifier code
"""
import io, random
import captcha.image

_DEFAULT_LENGTH = 4  # characters length
_DEFAULT_WIDTH = 100 # image width
_DEFAULT_HEIGHT = 48 # image height
_DEFAULT_FONTS = (38, 42, 48) # fonts set


# image creater
def createimage(chars, width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT, format='png'):
    """
        generate image data by input chars
    :param chars:
    :return:
    """
    _captcha = captcha.image.ImageCaptcha(width=width, height=height, font_sizes=_DEFAULT_FONTS)
    img = _captcha.generate_image(chars)

    data = io.BytesIO()
    img.save(data, format=format)
    return data.getvalue()


# rand number/alpha character generator
class _Rand:
    @staticmethod
    def num(nlen = _DEFAULT_LENGTH):
        """
            generate random numbers
        :param nlen:
        :return:
        """
        return str(random.randint(10**(nlen-1), 10**nlen-1))

    @staticmethod
    def alpha(nlen = _DEFAULT_LENGTH):
        """
            generate random alpha strings
        :param nlen:
        :return:
        """
        s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        rs = ''
        for i in range(nlen):
            rs += s[random.randint(0, len(s)-1)]

        return rs

    @staticmethod
    def alnum(nlen = _DEFAULT_LENGTH):
        """
            generate random alpha/number s
        :param nlen:
        :return:
        """
        s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        rs = ''
        for i in range(nlen):
            rs += s[random.randint(0, len(s)-1)]

        return rs


rand = _Rand


# verify code in image
class _Image:
    @staticmethod
    def num(nlen=_DEFAULT_LENGTH, width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT, format='png'):
        """
            generate random number image
        :param format:
        :return:
        """
        chars = rand.num(nlen)
        return chars, createimage(chars, width, height, format=format)

    @staticmethod
    def alpha(nlen=_DEFAULT_LENGTH, width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT, format='png'):
        """
            generate random alpha string image
        :param format:
        :return:
        """
        chars = rand.alpha(nlen)
        return chars, createimage(chars, width, height, format=format)

    @staticmethod
    def alnum(nlen=_DEFAULT_LENGTH, width=_DEFAULT_WIDTH, height=_DEFAULT_HEIGHT, format='png'):
        """
            generate random alpha/number image
        :param format:
        :return:
        """
        chars = rand.alnum(nlen)
        return chars, createimage(chars, width, height, format=format)


image = _Image


# verify code in sms
class _Sms:
    @staticmethod
    def send(phone, msg):
        """
            send msg to phone
        :param phone:
        :param msg:
        :return:
        """
        pass


sms = _Sms
