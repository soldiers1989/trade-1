import tornado.web
from app.quote import service, protocol


class QueryCurrentQuote(tornado.web.RequestHandler):
    """
        handler for query current quote of stock
    """
    def get(self):
        """
            get quote
        :return:
        """
        codes = self.get_argument('code').split(',')
        if len(codes) == 1:
            res, data = service.quotes.get(codes[0])
        else:
            res, data = service.quotes.gets(codes)

        if res:
            self.write(protocol.success(data=data))
        else:
            self.write(protocol.failed(msg=data))
