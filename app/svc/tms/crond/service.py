"""
    pub service
"""
import logging
import tornado.web, tornado.ioloop
from . import config, urls, timer

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start atm service
def start(port):
    # log start message
    logging.info('start atm service on port %d' % port)

    # start timer service
    timer.default.start()

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
