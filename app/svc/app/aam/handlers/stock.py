"""
    stock relate handlers
"""
import json
from .. import access, handler, daos, protocol


class StockListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        # get all stocks
        dao = daos.stock.StockDao(self.db)
        stocks = dao.list()

        # response
        self.write(protocol.success(data=stocks))


class StockGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        # get arguments
        id = self.get_argument('id')

        # get stock
        dao = daos.stock.StockDao(self.db)
        stock = dao.get(id=id)

        if stock is None:
            self.write(protocol.failed(msg='stock not exist'))
            return

        self.write(protocol.success(data=stock))


class StockAddHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        # parse stock data
        stocks = json.loads(self.request.body.decode())

        added, failed = [], []
        # add stocks
        dao = daos.stock.StockDao(self.db)
        for stock in stocks:
            try:
                dao.add(stock['id'], stock['name'], stock['jianpin'], stock['quanpin'], stock['status'], stock['limit'])
                added.append(stock['id'])
            except:
                failed.append(stock['id'])

        dao.commit()

        # response data
        data = {
            'added': added,
            'failed': failed
        }

        self.write(protocol.success(data=data))
