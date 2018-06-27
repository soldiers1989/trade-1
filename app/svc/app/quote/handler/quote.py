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
        try:
            codes = self.get_argument('code').split(',')
            if len(codes) == 1:
                data = service.quotes.get(codes[0])
            else:
                data = service.quotes.gets(codes)

            self.write(protocol.success(data=data))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
