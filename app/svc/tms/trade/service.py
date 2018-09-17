"""
    trade service
"""
import tornado.ioloop
import tornado.web, logging
from . import config, urls

# application settings
settings = {
    'autoreload': config.AUTORELOAD,
    'debug': config.DEBUG,
}


# start trade service
def start(port):
    # init logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(name)s][%(levelname)s]-%(message)s-[%(filename)s, %(lineno)d]')

    # log start message
    logging.info('start trade service on port %d' % port)

    app = tornado.web.Application(urls.handlers, **settings)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
