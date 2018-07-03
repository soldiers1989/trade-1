"""
    trade service
"""
import tornado.web
import tornado.ioloop

from app.trade import config, urls


# run quote service
def run(port):
    app = tornado.web.Application(urls.handlers, autoreload=config.AUTORELOAD, debug=config.DEBUG)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
