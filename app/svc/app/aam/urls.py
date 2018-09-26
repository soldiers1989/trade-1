from . import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),

    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),

    (r"/stock/list", handlers.stock.StockListHandler),
    (r"/stock/get", handlers.stock.StockGetHandler),
    (r"/stock/add", handlers.stock.StockAddHandler),


    (r"/trade/list", handlers.trade.ListHandler),
    (r"/trade/user/buy", handlers.trade.UserBuyHandler),
    (r"/trade/user/sell", handlers.trade.UserSellHandler),
    (r"/trade/user/close", handlers.trade.UserCloseHandler),
    (r"/trade/user/cancel", handlers.trade.UserCancelHandler),
    (r"/trade/sys/buy", handlers.trade.SysBuyHandler),
    (r"/trade/sys/sell", handlers.trade.SysSellHandler),
    (r"/trade/sys/close", handlers.trade.SysCloseHandler),
    (r"/trade/sys/cancel", handlers.trade.SysCancelHandler),
    (r"/trade/sys/bought", handlers.trade.SysBoughtHandler),
    (r"/trade/sys/sold", handlers.trade.SysSoldHandler),
    (r"/trade/sys/closed", handlers.trade.SysClosedHandler),
    (r"/trade/sys/canceled", handlers.trade.SysCanceledHandler),
    (r"/trade/sys/dropped", handlers.trade.SysDroppedHandler),
    (r"/trade/sys/expired", handlers.trade.SysExpiredHandler),
    (r"/trade/order/notify", handlers.trade.TradeNotifyHandler),

    (r"/order/list", handlers.order.ListHandler),
]
