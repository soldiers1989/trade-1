from app.aim import handlers

handlers = [
    (r"/user/login", handlers.user.LoginHandler),
    (r"/user/logout", handlers.user.LogoutHandler),

    (r"/admin/echo", handlers.admin.EchoHandler),
    (r"/admin/get/log", handlers.admin.GetLogHandler),
    (r"/admin/del/session", handlers.admin.DeleteSessionHandler),

    (r"/verifier/image", handlers.verifier.ImageHandler),
]
