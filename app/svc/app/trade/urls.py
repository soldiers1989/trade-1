from app.trade import  handlers

handlers = [
    (r"/login", handlers.trade.Login),
    (r"/logout", handlers.trade.Logout),
    (r"/status", handlers.trade.Status),
    (r"/query/gdxx", handlers.trade.QueryGdxx),
    (r"/query/dqzc", handlers.trade.QueryDqzc),
    (r"/query/dqcc", handlers.trade.QueryDqcc),
    (r"/query/drwt", handlers.trade.QueryDrwt),
    (r"/query/drcj", handlers.trade.QueryDrcj),
    (r"/query/kcwt", handlers.trade.QueryKcwt),
    (r"/query/lswt", handlers.trade.QueryLswt),
    (r"/query/lscj", handlers.trade.QueryLscj),
    (r"/query/jgd", handlers.trade.QueryJgd),
    (r"/query/gphq", handlers.trade.QueryGphq),
    (r"/order/xjmr", handlers.trade.OrderXjmr),
    (r"/order/xjmc", handlers.trade.OrderXjmc),
    (r"/order/sjmr", handlers.trade.OrderSjmr),
    (r"/order/sjmc", handlers.trade.OrderSjmc),
    (r"/order/cancel", handlers.trade.OrderCancel)
]
