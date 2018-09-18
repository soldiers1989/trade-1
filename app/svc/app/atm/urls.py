from . import handlers

handlers = [
    (r"/task/stock/sync/all", handlers.stock.SyncAllHandler),
]
