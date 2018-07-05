# 模块说明
    客户端接口服务，共有三种类型的接口服务：用户接口、数据接口、控制接口
    1.用户接口
        用户相关的服务接口，用户必须
    2.数据接口
    3.控制接口
   
    
# 接口说明
* 接口协议
    * 采用http协议，请求/响应模式
* 请求方式
    * 用户接口请求为POST方式
    * 数据接口请求为GET方式
    * 控制接口请求为GET方式
* 公共参数
    * 用户接口（登录接口除外）
        * sid: 字符串，登录成功返回的回话ID，必选
        * uid: 字符串，登录成功返回的用户ID，必选
    * 控制接口
        * token: 字符串，控制接口访问令牌，必选
* 响应格式
    * 成功响应格式:
    ``` 
        {
            “status”:0,
            “msg”:”status description”,
            “data”: <json数据>
        }
    ```
    * 失败响应格式：
    ```
        {
            “status”: -1,
            “msg”: ”status description”,
            “data”: <json数据>
        }
    ```
    
# 服务接口
## 用户登录 
* 接口说明
    * 注册用户登录
* 请求地址
    * POST /login
* 参数说明
    * user: 字符串，用户名（注册手机号），必选
    * pwd: 字符串, 登录密码, 必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: {
                "uid": <用户ID>
                "sid": <用户回话ID>
            }
        }
    ```
* 接口示例

## 用户登出
* 接口说明
    * 用户登出
* 请求地址
    * POST /logout
* 参数说明
    * 公共参数
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例


# 控制接口
## ECHO
* 接口说明
    * 检查服务是否存活
* 请求地址
    * GET /admin/echo
* 参数说明
    * 无
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例

## 获取访问日志
* 接口说明
    * 查看最近的访问日志
* 请求地址
    * GET /admin/get/log
* 参数说明
    * type: 字符串，取值范围info|error，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: [
                '.....',
                '.....'
            ]
        }
    ```
* 接口示例


## 清除SESSION
* 接口说明
    * 清除指定的session
* 请求地址
    * GET /admin/del/session
* 参数说明
    * sid: 字符串，待清除的session id，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例