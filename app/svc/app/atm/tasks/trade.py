"""
    robot trade service for user trade order
"""
import time, logging
from .. import task, rpc


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

    def _process_trades(self):
        """
            process user trades
        :return:
        """
        # get trades to process
        trades = self._trade.list(status='tobuy,tosell,toclose,cancelbuy,cancelsell,cancelclose')

        # process each trade
        for trade in trades:
            self._process_trade(trade)

    def _process_trade(self, trade):
        """
            process a user trade
        :param trade:
        :return:
        """
        if trade['status'] == 'tobuy':
            # select a new account
            account = self._account.select(type=trade['type'], stock=trade['stock_id'], optype=trade['optype'], oprice=trade['oprice'], ocount=trade['ocount'])
            # get stock name
            stockname = self._stock.get(trade['stock_id'])['name']
            # update trade status
            self._trade.sys_buy(trade['user_id'], trade['id'], account['account'])
            # add new buy trade order
            self._order.buy(account['account'], trade['tcode'], trade['stock_id'], stockname, trade['optype'], trade['ocount'], trade['oprice'], self._trade_notify_url, 'robot')
        elif trade['status'] in ['tosell', 'toclose']:
            # get stock name
            stockname = self._stock.get(trade['stock_id'])['name']
            # update trade status
            self._trade.sys_sell(trade['user_id'], trade['id'])
            # add new buy trade order
            self._order.buy(trade['account'], trade['tcode'], trade['stock_id'], stockname, trade['optype'], trade['ocount'], trade['oprice'], self._trade_notify_url, 'robot')
        elif trade['status'] == 'cancelbuy':
            pass
        elif trade['status'] == 'cancelsell':
            pass
        elif trade['status'] == 'cancelclose':
            pass
        else:
            pass

    def _process_orders(self):
        """
            process trade orders
        :return:
        """
        pass