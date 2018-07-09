# 模块说明
    客户端接口服务，包括以下类型的接口服务
    1.用户接口
        用户相关的服务接口，用户必须
    2.数据接口
    3.控制接口
    4.验证码接口
   
    
# 接口说明
* 接口协议
    * 采用http协议，请求/响应模式
* 请求方式
    * 用户接口请求为POST方式
    * 数据接口请求为GET方式
    * 控制接口请求为GET方式
* 公共参数
    * 用户接口（登录接口除外）
        * sid: 字符串，会话ID，必选
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
    
# 用户接口
## 查询会话ID
* 接口说明
    * 查询当前会话ID
* 请求地址
    * GET /user/sid
* 参数说明
    * 无
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: {
                "sid": <用户会话ID>
            }
        }
    ```
* 接口示例

## 查询用户是否存在
* 接口说明
    * 获取会话ID
* 请求地址
    * GET /user/sid
* 参数说明
    * 无
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: {
                "sid": <用户会话ID>
            }
        }
    ```
* 接口示例

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


# 验证码接口
## 图片验证码
* 接口说明
    * 获取和校验图片验证码 
* 请求地址
    * GET|POST /verify/image
* 参数说明
    * GET
        * i: 字符串，验证码用途唯一标识，必选
        * t: 字符串，验证码类别，n - number（数字），s - string(字母), ns - number/string(字母+数字)，可选
        * l: 整数，验证码长度，可选
        * w: 整数，图片宽度，可选
        * h: 整数，图片高度，可选
    * POST
        * i: 字符串，验证码用途唯一标识，必选
        * c: 字符串，用户输入的验证码，必选
* 成功返回
    * GET
        * 验证码图片
    * POST
    ```
        成功：
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
        失败：
        {
            “status”: <0,
            “msg”: ”图片验证码错误”,
            “data”: null
        }
    ```
* 接口示例

## 短信验证码
* 接口说明
    * 获取和校验短信验证码 
    * 验证码为数字
* 请求地址
    * GET|POST /verify/sms
* 参数说明
    * GET
        * p: 字符串，手机号，必选
        * l: 整数，验证码长度，可选
        * i: 字符串，验证码用途唯一标识，必选
    * POST
        * p: 字符串，手机号，必选
        * i: 字符串，验证码用途唯一标识，必选
        * c: 字符串，用户输入的验证码，必选
* 成功返回
    * GET
    ```
        成功：
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
        失败：
        {
            “status”: <0,
            “msg”: ”.....”,
            “data”: null
        }
    ```
    * POST
    ```
        成功：
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
        失败：
        {
            “status”: <0,
            “msg”: ”短信验证码错误”,
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

## 查询Redis
* 接口说明
    * 查询指定的redis
* 请求地址
    * GET /admin/redis/get
* 参数说明
    * t: 字符串，redis存储类型，None-string, h-hash, l-list, s-set, z-sorted set
    * n: 字符串，redis键值名称，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
* 接口示例


## 删除Redis
* 接口说明
    * 清除指定的redis
    
* 请求地址
    * GET /admin/redis/del
* 参数说明
    * n: 字符串，redis键值名称，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例

## 查询SESSION
* 接口说明
    * 清除指定的session
* 请求地址
    * GET /admin/session/get
* 参数说明
    * id: 字符串，待清除的session id，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
* 接口示例


## 删除SESSION
* 接口说明
    * 清除指定的session
* 请求地址
    * GET /admin/session/del
* 参数说明
    * id: 字符串，待清除的session id，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例

## 查询图片验证码
* 接口说明
     * 查询图片验证码信息
* 请求地址
    * GET /admin/verify/img/get
* 参数说明
    * sid: 字符串，待清除的session id，必选
    * n: 字符串，session扩展名，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
* 接口示例


## 删除图片验证码
* 接口说明
     * 删除图片验证码信息
* 请求地址
    * GET /admin/verify/img/del
* 参数说明
    * id: 字符串，待清除的session id，必选
    * n: 字符串，session扩展名，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例

## 查询短信验证码
* 接口说明
    * 查询短信验证码
* 请求地址
    * GET /admin/verify/sms/get
* 参数说明
    * p: 字符串，手机号，必选
    * n: 字符串，短信类别名称，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
* 接口示例


## 删除短信验证码
* 接口说明
    * 清除指定的session
* 请求地址
    * GET /admin/verify/sms/del
* 参数说明
    * p: 字符串，手机号，必选
    * n: 字符串，短信类别名称，必选
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
* 接口示例
