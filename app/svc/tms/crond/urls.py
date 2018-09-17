from . import handlers

handlers = [
    (r"/task/add", handlers.task.Add),
    (r"/task/del", handlers.task.Delete),
    (r"/task/clear", handlers.task.Clear),

    (r"/task/enable", handlers.task.Enable),
    (r"/task/disable", handlers.task.Disable),
    (r"/task/execute", handlers.task.Execute),
    (
        r"/task/callback", handlers.task.Callback),

    (r"/task/status", handlers.task.Status),
    (r"/task/detail", handlers.task.Detail),
]
