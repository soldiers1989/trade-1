"""
    quote service
"""
import tornado.web
import tornado.ioloop

from app.quote import config, urls


# run quote service
def run():
    app = tornado.web.Application(urls.handlers, autoreload=config.AUTORELOAD, debug=config.DEBUG)
    app.listen(config.PORT)
    tornado.ioloop.IOLoop.current().start()
