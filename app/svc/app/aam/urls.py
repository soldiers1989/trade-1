from . import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),

    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),

    (r"/stock/list", handlers.stock.StockListHandler),
    (r"/stock/get", handlers.stock.StockGetHandler),
    (r"/stock/add", handlers.stock.StockAddHandler),

    (r"/account/list", handlers.account.ListHandler),
    (r"/account/select", handlers.account.SelectHandler),

    (r"/order/list", handlers.order.ListHandler),
    (r"/order/place", handlers.order.PlaceHandler),
    (r"/order/cancel", handlers.order.CancelHandler),
    (r"/order/notify", handlers.order.NotifyHandler),
    (r"/order/ocode", handlers.order.OCodeHandler),

    (r"/trade/list", handlers.trade.ListHandler),

    (r"/trade/user/buy", handlers.trade.UserBuyHandler),
    (r"/trade/user/sell", handlers.trade.UserSellHandler),
    (r"/trade/user/cancel", handlers.trade.UserCancelHandler),

    (r"/trade/sys/buy", handlers.trade.SysBuyHandler),
    (r"/trade/sys/sell", handlers.trade.SysSellHandler),
    (r"/trade/sys/cancel", handlers.trade.SysCancelHandler),
    (r"/trade/sys/drop", handlers.trade.SysDropHandler),

    (r"/trade/order/bought", handlers.trade.OrderBoughtHandler),
    (r"/trade/order/sold", handlers.trade.OrderSoldHandler),
    (r"/trade/order/canceled", handlers.trade.OrderCanceledHandler),
    (r"/trade/order/expired", handlers.trade.OrderExpiredHandler),
]
