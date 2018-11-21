"""
    risk manager
"""
import json
from .. import access, handler, protocol, risker, models


class HoldsHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get trade list want to control risk
        :return:
        """
        with models.db.create() as d:
            # sql for tasks
            sql = 'select a.id, a.user_id, b.user, c.id as scode, c.name as sname, d.lever, d.wline, d.sline, a.tcode, a.optype, a.oprice, a.ocount, a.hprice, a.hcount, a.fcount, ' \
                  'a.bprice, a.bcount, a.sprice, a.scount, a.margin, a.amargin, a.ofee, a.dday, a.dfee, a.tprofit, a.sprofit, a.account, a.status, a.ctime, a.mtime ' \
                  'from tb_user_trade a, tb_user b, tb_stock c, tb_trade_lever d ' \
                  'where (a.status="hold" or a.status="toclose" or a.status="closing"or a.status="cancelclose") and a.user_id=b.id and a.stock_id=c.id and a.id=d.trade_id'


            # get hold status trade list
            data = models.model.RawModel.select(d, sql)

            # response data
            self.write(protocol.success(msg='success', data=data))


class GetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get risk management trade list
        :return:
        """
        # get parameters
        type = self.get_argument('type', None)
        type = None if type == '' else type

        # get trade list
        data = risker.get(type)

        with models.db.create() as d:
            # get holding trade list from database
            holds = models.UserTrade.filter(d, status__in=('hold','toclose','closing','cancelclose','closed')).all()
            holds = {trade['id']: trade for trade in holds}

            # process risk data
            for item in data:
                if item['id'] in holds.keys():
                    del holds[item['id']]['slog']
                    item.update(holds[item['id']])

            # response data
            self.write(protocol.success(msg='success', data=data))


class SetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            set risk management trade list
        :return:
        """
        # get parameters
        type = self.get_argument('type')
        # get trade list from body content
        trades = json.loads(self.request.body.decode())
        # set trade list to risker
        risker.set(type, trades)
        self.write(protocol.success(msg='success'))
