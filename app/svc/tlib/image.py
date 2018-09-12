import io
import captcha.image


def create(chars, width, height, fontsizes, format='png'):
    """
        generate image data by input chars
    :param chars: str, characters for image
    :param width: int, width of image in pixels
    :param height: int, height of image in pixels
    :param fontsizes: list/tupple, font size set for image
    :param format: str, file format, default png
    :return:
        bytes, image data
    """
    _captcha = captcha.image.ImageCaptcha(width=width, height=height, font_sizes=fontsizes)
    img = _captcha.generate_image(chars)

    data = io.BytesIO()
    img.save(data, format=format)
    return data.getvalue()
