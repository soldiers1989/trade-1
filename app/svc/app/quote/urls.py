from app.quote.handler import *

handlers = [
    (r"/status", status.QueryStatus),
    (r"/current", quote.QueryCurrentQuote)
]