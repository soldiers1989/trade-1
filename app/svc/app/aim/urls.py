from app.aim import handlers

handlers = [
    (r"/user/sid", handlers.user.GetSIDHandler),
    (r"/user/register", handlers.user.RegisterHandler),
    (r"/user/login", handlers.user.LoginHandler),
    (r"/user/logout", handlers.user.LogoutHandler),

    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/log/get", handlers.admin.LogGetHandler),
    (r"/admin/redis/get", handlers.admin.RedisGetHandler),
    (r"/admin/redis/del", handlers.admin.RedisDelHandler),
    (r"/admin/session/get", handlers.admin.SessionGetHandler),
    (r"/admin/session/del", handlers.admin.SessionDelHandler),
    (r"/admin/sessionext/get", handlers.admin.SessionExtGetHandler),
    (r"/admin/sessionext/del", handlers.admin.SessionExtDelHandler),
    (r"/admin/sms/get", handlers.admin.SmsGetHandler),
    (r"/admin/sms/del", handlers.admin.SmsDelHandler),

    (r"/verify/sms", handlers.verify.SmsHandler),
    (r"/verify/image", handlers.verify.ImageHandler),
]
