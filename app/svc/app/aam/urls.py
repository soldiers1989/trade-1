from app.aam import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/log/get", handlers.admin.LogGetHandler),
    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),

    (r"/trade/buy", handlers.trade.BuyHandler),
]
