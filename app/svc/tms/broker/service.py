"""
    web service
"""
import logging
import tornado.web, tornado.ioloop
from . import config, urls

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# setup environment
def _setup():
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')


# start broker service
def start(port, mode=config):
    # setup environment
    _setup()

    # log start message
    logging.info('start broker service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
