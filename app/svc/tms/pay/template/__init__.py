import os, tornado.template


_loader = tornado.template.Loader(os.path.dirname(__file__)+"/page")


def loadpage(page, **values):
    """

    :param page:
    :param values:
    :return:
    """
    return _loader.load(page).generate(**values)
