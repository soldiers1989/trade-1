from app.atm import handlers

handlers = [
    (r"/sync/stock/list", handlers.SyncStockList),

]
