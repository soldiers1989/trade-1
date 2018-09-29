"""
    trade service
"""
import tornado.ioloop
import tornado.web, logging
from . import config, urls, trader

# application settings
settings = {
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


def _setup():
    """
        setup running environment
    :return:
    """
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')

    # init trader
    trader.setup()


# start trade service
def start(port):
    # setup
    _setup()

    # log start message
    logging.info('start trade service on port %d' % port)

    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
