# -*- coding: utf-8 -*-
import uuid, json
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
# 访问秘钥，申请后修改
ACCESS_KEY_ID = "LTAI1a9jq8D6W4Ww"
ACCESS_KEY_SECRET = "cBXJgvFv4RtXZQozCri8i3X70D7duX"


# 服务地址
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"


# 初始化服务
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

# 发送客户端实例
_acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


class SmsAliyunError(Exception):
    pass

def send(phone, sign_name, template_code, template_param=None):
    """
        send message
    :param phone:
    :param sign_name:
    :param template_code:
    :param template_param:
    :return:
    """
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填
    business_id = uuid.uuid4()
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone)

    # 调用短信发送接口，返回json
    smsResponse = json.loads(_acs_client.do_action_with_exception(smsRequest).decode())

    # 检查发送结果
    if smsResponse['Code'] != 'OK':
        raise SmsAliyunError('%s,%s,%s-%s' % (phone, sign_name, template_code, smsResponse['Message']))

    # 返回数据
    return smsResponse


if __name__ == '__main__':
    params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(send("13000000000", "云通信测试", "SMS_5250008", params))




