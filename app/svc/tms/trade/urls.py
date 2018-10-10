from . import handlers

handlers = [
    (r"/account/add", handlers.trade.AddAccount),
    (r"/account/del", handlers.trade.DelAccount),
    (r"/account/clear", handlers.trade.ClearAccount),

    (r"/account/login", handlers.trade.LoginAccount),
    (r"/account/logout", handlers.trade.LogoutAccount),

    (r"/account/status", handlers.trade.StatusAccount),
    (r"/account/query", handlers.trade.Query),

    (r"/order/place", handlers.trade.Place),
    (r"/order/cancel", handlers.trade.Cancel),

    (r"/quote/query", handlers.trade.Quote),
]
