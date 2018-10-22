from . import handlers

handlers = [
    (r"/status", handlers.quote.QueryStatus),
    (r"/quote/level5", handlers.quote.QueryLevel5),
    (r"/quote/current", handlers.quote.QueryCurrent),
    (r"/quote/daily", handlers.quote.QueryDaily)
]
