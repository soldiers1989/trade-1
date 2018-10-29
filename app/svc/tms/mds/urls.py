from . import handlers

handlers = [
    (r"/stock/list", handlers.stock.List),
    (r"/stock/quotes", handlers.stock.Quotes),
    (r"/stock/quote", handlers.stock.Quote),
    (r"/stock/ticks", handlers.stock.Ticks),
    (r"/stock/kdata", handlers.stock.KData),
]

