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
        try:
            data = service.quotes.status()
            self.write(protocol.success(data=data))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
