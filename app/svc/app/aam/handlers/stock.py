"""
    stock relate handlers
"""
import json
from .. import access, handler, protocol, models


class StockListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        with models.db.create() as d:
            # get all stocks
            stocks = models.Stock.filter(d, **self.cleaned_arguments).all()

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

        with models.db.create() as d:
            # get stock by id
            stock = models.Stock.filter(d, id=id).one()
            if stock is None:
                self.write(protocol.failed(msg='stock not exist'))
            else:
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

        with models.db.atomic() as d:
            existed, added, fails = 0, 0, []
            # get all stocks
            localstocks = models.Stock.all(d)
            existids = [s.id for s in localstocks]

            # add not exist stocks
            for stock in stocks:
                if stock['id'] not in existids:
                    try:
                        models.Stock(**stock).save(d)
                        added += 1
                    except Exception as e:
                        fails.append(stock['id'])
                else:
                    existed += 1

            # response data
            data = {
                'total': len(stocks),
                'exist': existed,
                'added': added,
                'failed': len(fails),
                'fails': fails
            }

            self.write(protocol.success(data=data))
