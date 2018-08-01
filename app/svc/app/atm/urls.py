from app.atm import handlers

handlers = [
    (r"/stock/sync/all", handlers.stock.SyncAll),

]
