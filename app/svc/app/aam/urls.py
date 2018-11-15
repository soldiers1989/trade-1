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
    (r"/account/order/list", handlers.order.ListHandler),
    (r"/account/order/accounts", handlers.order.AccoutsHandler),
    (r"/account/order/update", handlers.order.UpdateHandler),
    (r"/account/order/take", handlers.order.TakeHandler),
    (r"/account/order/place", handlers.order.PlaceHandler),
    (r"/account/order/cancel", handlers.order.CancelHandler),
    (r"/account/order/notify", handlers.order.NotifyHandler),
    (r"/account/order/sending", handlers.order.SendingHandler),
    (r"/account/order/sent", handlers.order.SentHandler),
    (r"/account/order/dealt", handlers.order.DealtHandler),
    (r"/account/order/canceling", handlers.order.CancelingHandler),
    (r"/account/order/canceled", handlers.order.CanceledHandler),
    (r"/account/order/expired", handlers.order.ExpiredHandler),

    (r"/trade/list", handlers.trade.ListHandler),
    (r"/trade/clear", handlers.trade.ClearHandler),
    (r"/trade/update", handlers.trade.UpdateHandler),
    (r"/trade/user/buy", handlers.trade.UserBuyHandler),
    (r"/trade/user/sell", handlers.trade.UserSellHandler),
    (r"/trade/user/cancel", handlers.trade.UserCancelHandler),
    (r"/trade/sys/buy", handlers.trade.SysBuyHandler),
    (r"/trade/sys/sell", handlers.trade.SysSellHandler),
    (r"/trade/sys/cancel", handlers.trade.SysCancelHandler),
    (r"/trade/sys/drop", handlers.trade.SysDropHandler),

    (r"/trade/order/list", handlers.trade.OrderListHandler),
    (r"/trade/order/sent", handlers.trade.OrderSentHandler),
    (r"/trade/order/canceling", handlers.trade.OrderCancelingHandler),
    (r"/trade/order/bought", handlers.trade.OrderBoughtHandler),
    (r"/trade/order/sold", handlers.trade.OrderSoldHandler),
    (r"/trade/order/canceled", handlers.trade.OrderCanceledHandler),
    (r"/trade/order/expired", handlers.trade.OrderExpiredHandler),

    (r"/trade/order/update", handlers.trade.OrderUpdateHandler)
]
