"""
    robot trade service for user trade order
"""
import time, logging
from .. import task, rpc

_Dealt =  {
    "已成": "tdeal",
    "已撤": "tcanceled",
    "部撤": "pcanceled",
    "撤废": "fcanceled",
    "废单": "dropped"
}

class TradeService(task.Task):
    """
        trade service class
        config format:
        {
            interval: <schedule interval>,
            rpc: {
                trader: {
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
        # final status for dealt recognition
        self._dealt = config.get('dealt', _Dealt)

        # init trader rpc
        self._trader = rpc.TradeRpc(config['rpc']['trader']['baseurl'], config['rpc']['trader'].get('key'), config['rpc']['trader'].get('safety', False))
        self._trade = rpc.AamTradeRpc(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        self._order = rpc.AamOrderRpc(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        self._account = rpc.AamAccountRpc(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        self._stock = rpc.AamStockRpc(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

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

                # wait for next scheduling
                time.sleep(self._interval)
            except Exception as e:
                logging.error(str(e))

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
        # get trades to process
        trades = self._trade.list(status__in='tobuy,tosell,toclose,cancelbuy,cancelsell,cancelclose')

        # process each trade
        for trade in trades:
            self._process_trade(trade)

    def _process_trade(self, trade):
        """
            process a user trade
        :param trade:
        :return:
        """
        try:
            logging.info('start process trade: %s', trade)
            if trade['status'] == 'tobuy':
                # select a new account
                account = self._account.select(type=trade['type'], stock=trade['stock_id'], optype=trade['optype'], oprice=trade['oprice'], ocount=trade['ocount'])
                # get stock name
                stockname = self._stock.get(trade['stock_id'])['name']
                # update trade status
                self._trade.sys_buy(trade['user_id'], trade['id'], account['account'])
                # add new buy trade order
                self._order.buy(account['account'], trade['tcode'], trade['stock_id'], stockname, trade['optype'], trade['ocount'], trade['oprice'], self._trade_notify_url, 'sys')
            elif trade['status'] in ['tosell', 'toclose']:
                # get stock name
                stockname = self._stock.get(trade['stock_id'])['name']
                # update trade status
                self._trade.sys_sell(trade['user_id'], trade['id'])
                # add new buy trade order
                self._order.sell(trade['account'], trade['tcode'], trade['stock_id'], stockname, trade['optype'], trade['ocount'], trade['oprice'], self._trade_notify_url, 'sys')
            elif trade['status'] in ['cancelbuy', 'cancelsell, cancelclose']:
                # update trade status
                self._trade.sys_cancel(trade['user_id'], trade['id'])
                # get relate orders
                orders = self._order.list(status__in='notsend,tosend,sending,sent')
                # cancel order
                for order in orders:
                    self._order.cancel(order['id'], 'sys')
            else:
                pass
            logging.info('end process trade: %s', trade)
        except Exception as e:
            logging.info('exception process trade: %s', trade)

    def _process_orders(self):
        """
            process trade orders
        :return:
        """
        logging.info('start process orders')
        # get orders to process
        orders = self._order.list(status__in='notsend,tocancel')

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
                resp = self._order.notify(order['id'], 'tosend', 'sys')
                logging.info('update order: %s', resp)
                # place order
                resp = self._trader.place(order['account'], order['otype'], order['optype'], order['scode'], order['oprice'], order['ocount'])
                logging.info('place order: %s', resp)
                # update order code
                resp = self._order.update(order['id'], 'sent', 'sys', ocode=resp[0].wtbh)
                logging.info('update order: %s', resp)
            elif order['status'] == 'tocancel':
                # update order status
                resp = self._order.notify(order['id'], 'canceling', 'sys')
                logging.info('update order: %s', resp)
                # cancel order
                resp = self._trader.cancel(order['account'], order['scode'], order['ocode'])
                logging.info('cancel order: %s', resp)
            else:
                pass
            logging.info('end process order: %s', order)
        except Exception as e:
            logging.info('exception process order: %s', order)

    def _process_dealts(self):
        """
            process dealed orders
        :return:
        """
        logging.info('start process dealts')
        # get local orders to process
        localorders = self._order.list(status__in='tosend,sending,sent,canceling')

        # get order relate accounts
        accounts = []
        for order in localorders:
            if order['account'] is not None and order['account'] not in accounts:
                accounts.append(order['account'])

        # get remote orders to process
        remoteorders = {}
        for account in accounts:
            try:
                orders = self._trader.query_drwt(account)
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
                if lorder['ocode'] == rorder.wtbh:
                    try:
                        status = self._dealt.get(lorder['ztsm'])
                        if status is not None:
                            resp = self._order.notify(order['id'], status, 'sys', lorder.cjsl, lorder.cjjg)
                            logging.info('notify dealt order: %s', resp)
                    except Exception as e:
                        logging.info('notify dealt order failed, error: %s', str(e))
                    break

        logging.info('end process dealts')
