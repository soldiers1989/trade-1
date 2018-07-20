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
    (r"/user/cpwd", handlers.user.ChangePwdHandler),
    (r"/user/fpwd", handlers.user.FindPwdHandler),
    (r"/user/bank/get", handlers.user.GetBankHandler),
    (r"/user/bank/add", handlers.user.AddBankHandler),
    (r"/user/bank/del", handlers.user.DelBankHandler),
    (r"/user/coupon/get", handlers.user.GetCouponHandler),
    (r"/user/bill/get", handlers.user.GetBillHandler),
    (r"/user/charge/get", handlers.user.GetChargeHandler),
    (r"/user/draw/get", handlers.user.GetDrawHandler),
    (r"/user/stock/get", handlers.user.GetStockHandler),

    (r"/verify/gsms", handlers.verify.GeneralSmsHandler),
    (r"/verify/usms", handlers.verify.UserSmsHandler),
    (r"/verify/code", handlers.verify.CodeHandler),
    (r"/verify/gimg", handlers.verify.GeneralImageHandler),
    (r"/verify/simg", handlers.verify.SessionImageHandler),
]
