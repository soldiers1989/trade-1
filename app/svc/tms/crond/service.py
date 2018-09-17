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
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')

    # log start message
    logging.info('start crond service on port %d' % port)

    # start timer service
    timer.default.start()

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
