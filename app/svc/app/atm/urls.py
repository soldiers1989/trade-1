from . import handlers

handlers = [
    (r"/task/sync/stock/all/sina", handlers.task.SyncSinaAllStock),
    (r"/task/sync/stock/all/cninfo", handlers.task.SyncCNInfoAllStock),
]
