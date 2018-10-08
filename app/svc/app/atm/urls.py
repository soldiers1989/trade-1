from . import handlers

handlers = [
    (r"/task/stock/sync/all", handlers.stock.SyncAllHandler),
    (r"/task/trade/start", handlers.trade.StartHandler),
    (r"/task/trade/stop", handlers.trade.StopHandler),
]
