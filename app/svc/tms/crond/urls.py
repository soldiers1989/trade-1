from . import handlers

handlers = [
    (r"/remote/add", handlers.task.Add),
    (r"/remote/status", handlers.task.Status),
    (r"/remote/enable", handlers.task.Enable),
    (r"/remote/disable", handlers.task.Disable),
    (r"/remote/execute", handlers.task.Execute),
    (r"/remote/callback", handlers.task.Callback),
]
