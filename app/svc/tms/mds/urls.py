from . import handlers

handlers = [
    (r"/stock/list", handlers.stock.List),
    (r"/stock/quote", handlers.stock.Quote),
    (r"/stock/ticks", handlers.stock.Ticks),
    (r"/stock/kline", handlers.stock.KLine),
]

