from app.quote import handlers

handlers = [
    (r"/status", handlers.quote.QueryStatus),
    (r"/quote", handlers.quote.QueryCurrent)
]
