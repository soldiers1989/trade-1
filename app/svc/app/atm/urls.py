from . import handlers

handlers = [
    (r"/task/status", handlers.task.Status),
    (r"/task/enable", handlers.task.Enable),
    (r"/task/disable", handlers.task.Disable),
    (r"/task/execute", handlers.task.Execute)
]
