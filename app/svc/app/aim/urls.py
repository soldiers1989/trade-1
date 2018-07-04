from app.aim import handlers

handlers = [
    (r"/echo", handlers.echo.EchoHandler),
    (r"/user/login", handlers.user.LoginHandler),
    (r"/user/logout", handlers.user.LogoutHandler)
]
