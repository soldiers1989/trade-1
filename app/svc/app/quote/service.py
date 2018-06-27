"""
    quote service
"""
import tornado.web
import tornado.ioloop

from app.quote import config, urls
from lib.stock import quote

# quotes object for service
quotes = quote.quotes.Quotes()


# run quote service
def run():
    app = tornado.web.Application(urls.handlers)
    app.listen(config.PORT)
    tornado.ioloop.IOLoop.current().start()
