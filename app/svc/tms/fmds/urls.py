from . import handlers

handlers = [
    (r"/status", handlers.quote.QueryStatus),
    (r"/stock/list", handlers.quote.QueryLevel5),
]
