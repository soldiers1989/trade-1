"""
    pub service
"""
import tornado.web
import tornado.ioloop, logging

from . import config, urls

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# setup running environments
def _setup():
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')


# start aim service
def start(port):
    # setup
    _setup()

    # log start message
    logging.info('start aim service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
