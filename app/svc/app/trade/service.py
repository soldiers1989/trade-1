"""
    trade service
"""
import tornado.web
import tornado.ioloop

from app.trade import config, urls


# application settings
settings = {
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start trade service
def start(port):
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
