import logging
import traceback
from .. import rsakey

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse


def pay():
    return pagepay()

def apppay():
    """
       设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
       """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016092000553959'
    alipay_client_config.app_private_key = rsakey.load('alipay/private')
    alipay_client_config.alipay_public_key = rsakey.load('alipay/notify')

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logging.root)

    model = AlipayTradeAppPayModel()
    model.timeout_express = "90m"
    model.total_amount = "9.00"
    model.seller_id = "2088301194649043"
    model.product_code = "QUICK_MSECURITY_PAY"
    model.body = "Iphone6 16G"
    model.subject = "iphone"
    model.out_trade_no = "201800000001201"
    request = AlipayTradeAppPayRequest(biz_model=model)
    response = client.sdk_execute(request)
    return response
    print("alipay.trade.app.pay response:" + response)

def pagepay():
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016092000553959'
    alipay_client_config.app_private_key = rsakey.load('alipay/private')
    alipay_client_config.alipay_public_key = rsakey.load('alipay/notify')

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logging.root)

    """
       页面接口示例：alipay.trade.page.pay
       """
    # 对照接口文档，构造请求对象
    model = AlipayTradePagePayModel()
    model.out_trade_no = "pay201805020000228"
    model.total_amount = 1
    model.subject = "测试"
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    settle_detail_info = SettleDetailInfo()
    settle_detail_info.amount = 1
    settle_detail_info.trans_in_type = "userId"
    settle_detail_info.trans_in = "2088102176453773"
    settle_detail_infos = list()
    settle_detail_infos.append(settle_detail_info)
    settle_info = SettleInfo()
    settle_info.settle_detail_infos = settle_detail_infos
    model.settle_info = settle_info
    #sub_merchant = SubMerchant()
    #sub_merchant.merchant_id = ""
    #model.sub_merchant = sub_merchant
    request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    response = client.page_execute(request, http_method="POST")
    return response


def tradepay():
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016092000553959'
    alipay_client_config.app_private_key = rsakey.load('alipay/private')
    alipay_client_config.alipay_public_key = rsakey.load('alipay/notify')

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logging.root)

    # 对照接口文档，构造请求对象
    model = AlipayTradePayModel()
    model.auth_code = "280976506431097692"
    model.body = "Iphone6 16G"
    goods_list = list()
    goods1 = GoodsDetail()
    goods1.goods_id = "apple-01"
    goods1.goods_name = "ipad"
    goods1.price = 10
    goods1.quantity = 1
    goods_list.append(goods1)
    model.goods_detail = goods_list
    model.operator_id = "yx_001"
    model.out_trade_no = "20180510AB014"
    model.product_code = "FACE_TO_FACE_PAYMENT"
    model.scene = "bar_code"
    model.store_id = ""
    model.subject = "huabeitest"
    model.timeout_express = "90m"
    model.total_amount = 1
    request = AlipayTradePayRequest(biz_model=model)
    # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # udf_params = dict()
    # from alipay.aop.api.constant.ParamConstants import *
    # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # request.udf_params = udf_params
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        response = AlipayTradePayResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        print(response.body)
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
