from . import handlers

handlers = [
    (r"/admin/echo", handlers.admin.EchoHandler),

    (r"/user/session/get", handlers.user.SessionGetHandler),

    (r"/user/exist", handlers.user.UserExistHandler),
    (r"/user/register", handlers.user.UserRegisterHandler),

    (r"/user/login", handlers.user.UserLoginHandler),
    (r"/user/logout", handlers.user.UserLogoutHandler),

    (r"/user/verify", handlers.user.UserVerifyHandler),

    (r"/user/pwd/change", handlers.user.UserPwdChangeHandler),
    (r"/user/pwd/reset", handlers.user.UserPwdResetHandler),

    (r"/user/bank/get", handlers.user.GetBankHandler),
    (r"/user/bank/add", handlers.user.AddBankHandler),
    (r"/user/bank/del", handlers.user.DelBankHandler),

    (r"/user/coupon/get", handlers.user.GetCouponHandler),
    (r"/user/bill/get", handlers.user.GetBillHandler),
    (r"/user/charge/get", handlers.user.GetChargeHandler),
    (r"/user/draw/get", handlers.user.GetDrawHandler),
    (r"/user/stock/get", handlers.user.GetStockHandler),

    (r"/verify/sms", handlers.verify.VerifySmsHandler),
    (r"/verify/id/get", handlers.verify.VerifyIDGetHandler),
    (r"/verify/image/general", handlers.verify.VerifyImageGeneralHandler),
    (r"/verify/image/session", handlers.verify.VerifyImageSessionHandler),
]
