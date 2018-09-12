"""
    pub service
"""
import tornado.web
import tornado.ioloop

from . import config, urls, logger

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start aim service
def start(port):
    # log start message
    logger.info('start aim service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
