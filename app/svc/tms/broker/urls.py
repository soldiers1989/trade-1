from . import handlers

handlers = [
    (r"/trade/start", handlers.trade.StartHandler),
    (r"/trade/stop", handlers.trade.StopHandler),

    (r"/trade/register", handlers.trade.RegisterHandler),
    (r"/trade/login", handlers.trade.LoginHandler),
    (r"/trade/logout", handlers.trade.LogoutHandler),

    (r"/trade/transfer", handlers.trade.TransferHandler),
    (r"/trade/query", handlers.trade.QueryHandler),
    (r"/trade/place", handlers.trade.PlaceHandler),
    (r"/trade/cancel", handlers.trade.CancelHandler),

    (r"/trade/clear", handlers.trade.ClearHandler),
]
