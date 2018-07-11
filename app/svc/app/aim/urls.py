from app.aim import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),

    (r"/user/sid", handlers.user.GetSIDHandler),
    (r"/user/exist", handlers.user.UserExistHandler),
    (r"/user/register", handlers.user.RegisterHandler),
    (r"/user/vimg", handlers.user.UserExistHandler),
    (r"/user/vsms", handlers.user.UserExistHandler),
    (r"/user/login", handlers.user.LoginHandler),
    (r"/user/logout", handlers.user.LogoutHandler),

    (r"/verify/gsms", handlers.verify.GeneralSmsHandler),
    (r"/verify/usms", handlers.verify.UserSmsHandler),
    (r"/verify/code", handlers.verify.CodeHandler),
    (r"/verify/gimg", handlers.verify.GeneralImageHandler),
    (r"/verify/simg", handlers.verify.SessionImageHandler),
]
