from . import handlers

handlers = [
    (r"/sms/send", handlers.sms.Send),
]

