from app.aam import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/log/get", handlers.admin.LogGetHandler),
    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),

    (r"/trade/user/buy", handlers.trade.UserBuyHandler),
    (r"/trade/user/sell", handlers.trade.UserSellHandler),
    (r"/trade/user/cancel", handlers.trade.UserCancelHandler),

    (r"/trade/sys/buy", handlers.trade.CloseHandler),
    (r"/trade/sys/sell", handlers.trade.CloseHandler),
    (r"/trade/sys/close1", handlers.trade.CloseHandler),
    (r"/trade/sys/close2", handlers.trade.CloseHandler),
    (r"/trade/sys/cancel", handlers.trade.CloseHandler),

    (r"/trade/sys/bought", handlers.trade.CloseHandler),
    (r"/trade/sys/sold", handlers.trade.CloseHandler),
    (r"/trade/sys/closed", handlers.trade.CloseHandler),
    (r"/trade/sys/canceled", handlers.trade.CloseHandler),
]
