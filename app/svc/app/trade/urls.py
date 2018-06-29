from app.trade import handler

handlers = [
    (r"/login", handler.Login),
    (r"/logout", handler.Logout),
    (r"/status", handler.Status),
    (r"/query/gdxx", handler.QueryGdxx),
    (r"/query/dqzc", handler.QueryDqzc),
    (r"/query/dqcc", handler.QueryDqcc),
    (r"/query/drwt", handler.QueryDrwt),
    (r"/query/drcj", handler.QueryDrcj),
    (r"/query/kcwt", handler.QueryKcwt),
    (r"/query/lswt", handler.QueryLswt),
    (r"/query/lscj", handler.QueryLscj),
    (r"/query/jgd", handler.QueryJgd),
    (r"/query/gphq", handler.QueryGphq),
    (r"/order/xjmr", handler.OrderXjmr),
    (r"/order/xjmc", handler.OrderXjmc),
    (r"/order/sjmr", handler.OrderSjmr),
    (r"/order/sjmc", handler.OrderSjmc),
]
