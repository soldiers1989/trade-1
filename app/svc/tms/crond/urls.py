from . import handlers

handlers = [
    (r"/task/list", handlers.task.List),
    (r"/task/load", handlers.task.Load),

    (r"/task/add", handlers.task.Add),
    (r"/task/update", handlers.task.Update),
    (r"/task/delete", handlers.task.Delete),
    (r"/task/clear", handlers.task.Clear),

    (r"/task/enable", handlers.task.Enable),
    (r"/task/disable", handlers.task.Disable),

    (r"/task/execute", handlers.task.Execute),
    (r"/task/callback", handlers.task.Callback),

    (r"/task/status", handlers.task.Status),
    (r"/task/detail", handlers.task.Detail),
]
