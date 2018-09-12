"""
    pub service
"""
import tornado.web
import tornado.ioloop

from . import config, urls, log

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start aam service
def start(port):
    # log start message
    log.info('start aam service on port %d' % port)

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
