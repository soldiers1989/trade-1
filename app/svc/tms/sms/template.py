"""
    message template for business
"""


business = {
    'aam': {
        'sign': '测试签名', # 业务签名
        'tpls': { # 短信内容模板
            'verify':{ # 验证码
                'tpl': '您的短信验证码 %s，1分钟内有效', # 短信模板
                'code': {
                    'aliyun': 'AT00001', # 阿里云模板代码
                    'tencent': 'TT00001' # 腾讯模板代码
                }
            },
            'blabla': {  # 其它模板
                'tpl': '您的短信验证码 %s，1分钟内有效',  # 短信模板
                'code': {
                    'aliyun': 'AT00001',  # 阿里云模板代码
                    'tencent': 'TT00001'  # 腾讯模板代码
                }
            }
        }
    }
}

