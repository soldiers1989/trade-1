import tornado.web
from app.quote import service, protocol


class QueryStatus(tornado.web.RequestHandler):
    """
        handler for query quote service status
    """
    def get(self):
        """
            get quote service status
        :return:
        """
        data = service.quotes.status()
        self.write(protocol.success(data=data))
