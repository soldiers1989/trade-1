from . import handlers

handlers = [
    (r"/task/stock/sync/all", handlers.stock.SyncAllHandler),

    (r"/task/order/take", handlers.order.TakeHandler),
    (r"/task/order/place", handlers.order.PlaceHandler),
    (r"/task/order/notify", handlers.order.NotifyHandler),

    (r"/task/trade/take", handlers.trade.TakeHandler),
    (r"/task/trade/place", handlers.trade.PlaceHandler),
    (r"/task/trade/notify", handlers.trade.NotifyHandler),
    (r"/task/trade/clear", handlers.trade.ClearHandler),
    (r"/task/trade/expire", handlers.trade.ExpireHandler),

    (r"/task/risk/check", handlers.risker.CheckHandler),
]
