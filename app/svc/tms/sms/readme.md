# 模块说明
    短信消息服务(short message service)

# 依赖模块
* tornado
* json
*


# 接口说明
* 接口通讯采用http协议，无状态请求/响应模式
* 请求为GET方式
* 响应为JSON格式内容
    * 成功响应格式:
    ``` 
        {
            “status”:0,
            “msg”:”status description”,
            “data”: data
        }
    ```
    * 失败响应格式：
    ```
        {
            “status”: -1,
            “msg”: ”status description”,
            “data”: data
        }
    ```
    
# 服务接口

## 服务状态
* 接口说明
    * 发送短信
* 请求地址
    * GET /sms/send
* 参数说明
    * 无
* 接口示例
