from app.api import handlers

handlers = [
    (r"/echo", handlers.echo.EchoHandler),
    (r"/trade/user/buy", handlers.trade.UserBuyHandler),
    (r"/trade/user/sell", handlers.trade.UserSellHandler)
]
