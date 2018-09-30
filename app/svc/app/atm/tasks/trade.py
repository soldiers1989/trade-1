"""
    robot trade service for user trade order
"""
from .. import task, rpc


class TradeService(task.Task):
    """
        trade service class
        config format:
        {
            rpc: {
                trader: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                },
                trade: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                },
                order: {
                    baseurl: <baseurl>
                    key: <key>
                    safety: <True|False>
                }
            }
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
        confg = kwargs.get('config')

        # init trader rpc
        self._trader = rpc.TradeRpc(confg['rpc']['trader']['baseurl'], confg['rpc']['trader'].get('key'), confg['rpc']['trader'].get('safety', False))
        self._trade = rpc.AamTradeRpc(confg['rpc']['trade']['baseurl'], confg['rpc']['trade'].get('key'), confg['rpc']['trade'].get('safety', False))
        self._order = rpc.AamOrderRpc(confg['rpc']['order']['baseurl'], confg['rpc']['order'].get('key'), confg['rpc']['order'].get('safety', False))

        # init super
        super().__init__(*args, **kwargs)

    def execute(self):
        pass