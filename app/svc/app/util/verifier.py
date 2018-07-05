"""
    generate verifier code
"""
import io, random
import captcha.image

_LENGTH = 4

_WIDTH = 100
_HEIGHT = 48
_FONTS = (38, 42, 48)


def randn(nlen = _LENGTH):
    """
        generate random numbers
    :param nlen:
    :return:
    """
    return str(random.randint(10**(nlen-1), 10**nlen-1))


def rands(nlen = _LENGTH):
    """
        generate random strings
    :param nlen:
    :return:
    """
    s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    rs = ''
    for i in range(nlen):
        rs += s[random.randint(0, len(s)-1)]

    return rs


def randns(nlen = _LENGTH):
    """
        generate random string/number s
    :param nlen:
    :return:
    """
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    rs = ''
    for i in range(nlen):
        rs += s[random.randint(0, len(s)-1)]

    return rs


def image(chars, width=_WIDTH, height=_HEIGHT, format='png'):
    """
        generate image data by input chars
    :param chars:
    :return:
    """
    _captcha = captcha.image.ImageCaptcha(width=width, height=height, font_sizes=_FONTS)
    img = _captcha.generate_image(chars)

    data = io.BytesIO()
    img.save(data, format=format)
    return data.getvalue()


def randnimg(nlen=_LENGTH, width=_WIDTH, height=_HEIGHT, format='png'):
    """
        generate random number image
    :param format:
    :return:
    """
    return image(randn(nlen), width, height, format=format)


def randsimg(nlen=_LENGTH, width=_WIDTH, height=_HEIGHT, format='png'):
    """
        generate random alpha string image
    :param format:
    :return:
    """
    return image(rands(nlen), width, height, format=format)


def randnsimg(nlen=_LENGTH, width=_WIDTH, height=_HEIGHT, format='png'):
    """
        generate random alpha/number image
    :param format:
    :return:
    """
    return image(randns(nlen), width, height, format=format)
