from app.aim import handlers

handlers = [
    (r"/user/sid", handlers.user.GetSIDHandler),
    (r"/user/exist", handlers.user.UserExistHandler),
    (r"/user/register", handlers.user.RegisterHandler),
    (r"/user/vimg", handlers.user.UserExistHandler),
    (r"/user/vsms", handlers.user.UserExistHandler),
    (r"/user/login", handlers.user.LoginHandler),
    (r"/user/logout", handlers.user.LogoutHandler),

    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/log/get", handlers.admin.LogGetHandler),
    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),
    (r"/admin/session/get", handlers.admin.SessionGetHandler),
    (r"/admin/session/del", handlers.admin.SessionDelHandler),
    (r"/admin/verify/img/get", handlers.admin.VerifyImgGetHandler),
    (r"/admin/verify/img/del", handlers.admin.VerifyImgDelHandler),
    (r"/admin/verify/sms/get", handlers.admin.VerifySmsGetHandler),
    (r"/admin/verify/sms/del", handlers.admin.VerifySmsDelHandler),

    (r"/verify/sms", handlers.verify.SmsHandler),
    (r"/verify/image", handlers.verify.ImageHandler),
]
