"""
    pub service
"""
import tornado.web
import tornado.ioloop

from app.atm import config, urls, timer, log, tasks

# application settings
settings = {
    'cookie_secret': config.COOKIE_SECRET,
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start atm service
def start(port):
    # log start message
    log.info('start atm service on port %d' % port)

    # start timer service
    timer.default.start()

    # start web application
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
