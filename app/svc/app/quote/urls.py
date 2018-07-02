from app.quote import handler

handlers = [
    (r"/status", handler.QueryStatus),
    (r"/current", handler.QueryCurrent)
]
