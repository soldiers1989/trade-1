"""
    pub service
"""
import tornado.web
import tornado.ioloop, logging

from . import config, urls
from tlib import chttp

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}

# aysnc http client
asynchttp = chttp.CHttp()

# setup running environments
def _setup():
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')

    # init chttp
    asynchttp.start()


# start aam service
def start(port):
    # setup
    _setup()

    # log start message
    logging.info('start aam service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
