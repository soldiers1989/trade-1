"""
    service
"""
import tornado.web
import tornado.ioloop

from app.quote import config, urls


# application settings
settings = {
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start quote service
def start(port):
    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
