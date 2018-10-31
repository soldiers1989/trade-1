"""
    robot trade service for user trade order
"""
import time, logging, tms, app
from .. import task


class _Repr:
    def __init__(self, **filters):
        """
            init a represent object
        :param filters: dict, filter key->rename
        """
        self._filters = filters

    def format(self, obj):
        """
            use
        :param obj:
        :return:
        """
        if not isinstance(obj, dict):
            return str(obj)

        items = ['']
        for k, v in self._filters.items():
            items.append("%s: %s" % (str(v), str(obj.get(k))))
        return "\n\t".join(items) + '\n'

_repr_account = _Repr(id='ID', account='账户代码', name='账户名称', lmoney='账户余额')

_repr_trade = _Repr(id='ID', code='订单代码', user_id='用户ID', stock_id='股票代码', optype='价格类型', oprice='订单价格', ocount='订单数量',
                    hprice='持仓价格', hcount='持仓数量',bprice='买入价格', bcount='买入数量', sprice='卖出价格', scount='卖出数量', status='订单状态')

_repr_order = _Repr(id='ID', scode='股票代码', sname='股票名称', tcode='交易代码', otype='委托方向', optype='价格类型',
                    oprice='委托价格', ocount='委托数量', ocode='委托编号', dprice='成交价格', dcount='成交数量', status='委托状态')

_repr_drwt = _Repr(wtrq='委托日期', wtsj='委托时间', gddm='股东代码', zqdm='证券代码', zqmc='证券名称', mmbz='买卖标志', wtjg='委托价格', wtsl='委托数量',
                   wtbh='委托编号', cjsl='成交数量', cjjg='成交价格', cjje='成交金额', cdsl='撤单数量', cdbz='撤单标志', ztsm='状态说明')


class TradeService(task.Task):
    """
        trade service class
        config format:
        {
            interval: <schedule interval>,
            rpc: {
                trade: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                },
                aam: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                }
            },
            notify: {
                trade: <trade notify url>
            }
        }
    """
    def __init__(self, *args, **kwargs):
        """
            init trade service object
        :param args:
        :param kwargs:
        """
        # get config
        config = kwargs.get('config')

        # init schedule interval, default every 5s
        self._interval = config.get('interval', 5)
        # trade notify url
        self._trade_notify_url = config['notify']['trade']

        # init trader rpc
        self._trade = tms.rpc.Trade(config['rpc']['trade']['baseurl'], config['rpc']['trade'].get('key'), config['rpc']['trade'].get('safety', False))
        self._aam = app.rpc.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

        # init super
        super().__init__(*args, **kwargs)

    def execute(self):
        """
            execute robot trade service
        :return:
        """
        while not self._stopped:
            try:
                # schedule trade tasks
                self._schedule()
            except Exception as e:
                logging.error(str(e))
            # wait for next scheduling
            time.sleep(self._interval)

    def _schedule(self):
        """
            schedule trade task
        :return:
        """
        # process user trades
        self._process_trades()
        # process trade orders
        self._process_orders()
        # process dealt orders
        self._process_dealts()

    def _process_trades(self):
        """
            process user trades
        :return:
        """
        logging.info('start process trades')
        # get trades to process
        trades = self._aam.trade_list(status__in='tobuy,tosell,toclose,cancelbuy,cancelsell,cancelclose')
        logging.info('%s trades waiting to process.' % str(len(trades)))

        # process each trade
        for trade in trades:
            self._process_trade(trade)
        logging.info('end process trades')

    def _process_trade(self, trade):
        """
            process a user trade
        :param trade:
        :return:
        """
        try:
            logging.info('start process trade: %s', _repr_trade.format(trade))
            if trade['status'] == 'tobuy':
                # select a new account
                account = self._aam.account_select(type=trade['type'], stock=trade['stock_id'], optype=trade['optype'], oprice=trade['oprice'], ocount=trade['ocount'])
                logging.info('select account: %s', _repr_account.format(account))
                # get stock name
                stockname = self._aam.stock_get(id=trade['stock_id'])['name']
                # update trade status
                resp = self._aam.trade_sys_buy(user=trade['user_id'], trade=trade['id'], account=account['account'])
                logging.info('sys buy: %s', _repr_trade.format(resp))
                # add new buy trade order
                resp = self._aam.order_buy(account=account['account'], tcode=trade['code'], scode=trade['stock_id'], sname=stockname, optype=trade['optype'], ocount=trade['ocount'], oprice=trade['oprice'], callback=self._trade_notify_url, operator='sys')
                logging.info('order buy: %s', _repr_order.format(resp))
            elif trade['status'] in ['tosell', 'toclose']:
                # get stock name
                stockname = self._aam.stock_get(id=trade['stock_id'])['name']
                # update trade status
                resp = self._aam.trade_sys_sell(user=trade['user_id'], trade=trade['id'])
                logging.info('sys sell: %s', _repr_trade.format(resp))
                # add new buy trade order
                resp = self._aam.order_sell(account=trade['account'], tcode=trade['code'], scode=trade['stock_id'], sname=stockname, optype=trade['optype'], ocount=trade['ocount'], oprice=trade['oprice'], callback=self._trade_notify_url, operator='sys')
                logging.info('order sell: %s', _repr_order.format(resp))
            elif trade['status'] in ['cancelbuy', 'cancelsell', 'cancelclose']:
                # update trade status
                resp = self._aam.trade_sys_cancel(user=trade['user_id'], trade=trade['id'])
                logging.info('sys cancel: %s', _repr_trade.format(resp))
                # get relate orders
                orders = self._aam.order_list(status__in='notsend,tosend,sending,sent')
                # cancel order
                for order in orders:
                    resp = self._aam.order_cancel(id=order['id'], operator='sys')
                    logging.info('order cancel: %s', _repr_order.format(resp))
            else:
                pass
            logging.info('end process trade: %s', trade)
        except Exception as e:
            logging.info('exception process trade, error: %s', str(e))

    def _process_orders(self):
        """
            process trade orders
        :return:
        """
        logging.info('start process orders')
        # get orders to process
        orders = self._aam.order_list(status__in='notsend,tocancel')

        logging.info('%s orders waiting to process.' % str(len(orders)))

        # process each order
        for order in orders:
            self._process_order(order)
        logging.info('end process orders')

    def _process_order(self, order):
        """
            process order
        :param order: dict, order object
        :return:
        """
        try:
            logging.info('start process order: %s', order)
            if order['status'] == 'notsend':
                # update order status
                resp = self._aam.order_notify(id=order['id'], status='tosend', operator='sys')
                logging.info('update order: %s', _repr_order.format(resp))
                # place order
                resp = self._trade.place(account=order['account'], otype=order['otype'], ptype=order['optype'], zqdm=order['scode'], price=order['oprice'], count=order['ocount'])
                logging.info('place order: %s', resp)
                # update order code
                resp = self._aam.order_update(id=order['id'], status='sent', operator='sys', ocode=resp['wtbh'])
                logging.info('update order: %s', _repr_order.format(resp))
            elif order['status'] == 'tocancel':
                # update order status
                resp = self._aam.order_notify(id=order['id'], status='canceling', operator='sys')
                logging.info('update order: %s', _repr_order.format(resp))
                # cancel order
                resp = self._trade.cancel(account=order['account'], zqdm=order['scode'], orderno=order['ocode'])
                logging.info('cancel order: %s', resp)
            else:
                pass
            logging.info('end process order: %s', order)
        except Exception as e:
            logging.info('exception process order, error: %s', str(e))

    def _process_dealts(self):
        """
            process dealed orders
        :return:
        """
        logging.info('start process dealts')
        # get local orders to process
        localorders = self._aam.order_list(status__in='tosend,sending,sent,canceling')

        logging.info('%s orders waiting to dealt.' % str(len(localorders)))

        # get order relate accounts
        accounts = []
        for order in localorders:
            if order['account'] is not None and order['account'] not in accounts:
                accounts.append(order['account'])

        # get remote orders to process
        remoteorders = {}
        for account in accounts:
            try:
                orders = self._trade.query(account=account, type='drwt')
                remoteorders[account] = orders
            except Exception as e:
                logging.error('query drwt from account %s failed, error: %s' % (account, str(e)))

        # check local vs remote order status
        for lorder in localorders:
            # get remote relate account's orders
            rorders = remoteorders.get(lorder['account'])
            if rorders is None:
                continue

            # check remote order status relate with local order
            for rorder in rorders:
                if lorder['ocode'] == rorder['wtbh']:
                    try:
                        if rorder['ztsm'] in ['tdeal', 'tcanceled', 'pcanceled', 'fcanceled', 'dropped']:
                            resp = self._aam.order_notify(id=lorder['id'], status=rorder['ztsm'], operator='sys', dcount=rorder['cjsl'], dprice=rorder['cjjg'])
                            logging.info('notify dealt order: %s', _repr_order.format(resp))
                    except Exception as e:
                        logging.info('notify dealt order failed, error: %s', str(e))
                    break

        logging.info('end process dealts')
