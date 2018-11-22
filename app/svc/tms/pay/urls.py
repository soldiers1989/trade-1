from . import handlers

handlers = [
    (r"/pay", handlers.pay.PayHandler),
    (r"/notify", handlers.notify.NotifyHandler),
]

