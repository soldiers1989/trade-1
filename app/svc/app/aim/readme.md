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
    * 查询用户是否存在
* 请求地址
    * GET /user/exist
* 参数说明
    * phone: 字符串，注册手机号，必须
* 成功返回
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: {
                "exist": <true|false>
            }
        }
    ```
* 接口示例

## 用户登录 
* 接口说明
    * 注册用户登录
* 请求地址
    * POST /user/login
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
    * POST /user/logout
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

## 用户注册
* 接口说明
    * 用户注册，只支持手机号注册
* 请求地址
    * POST /user/register
* 参数说明
    * phone: 字符串，注册手机号，必选
    * pwd: 字符串, 登录密码, 必选
    * vcode: 字符串，手机验证码，必选
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
## 获取通用验证码
* 接口说明
    * 获取通用验证码 
* 请求地址
    * POST /verify/code
* 参数说明
    * POST
        * t: 字符串，验证码类型，n - number（数字），s - string(字母), ns - number/string(字母+数字)，必选
        * l: 整数，验证码长度，必选
* 成功返回
    * GET
        * 验证码图片
    * POST
    ```
        成功：
        {
            "status": 0,
            "msg": "success",
            "data": {
                "id": "806p1pfpd9rd8"
            }
        }
    ```
* 接口示例


## 获取和校验通用验证码图片
* 接口说明
    * 获取通用验证码图片、校验通用验证码
* 请求地址
    * GET|POST /verify/gimg
* 参数说明
    * GET
        * i: 字符串，验证码ID，获取通用验证码返回的ID，必选
        * w: 整数，图片宽度，必选
        * h: 整数，图片高度，必选
        * f: 字符串，验证码字号数字，用','分隔，例如 f=32,43,23，必选
    * POST
        * i: 字符串，验证码ID，必选
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

## 获取和校验会话验证码图片
* 接口说明
    * 获取会话验证码图片、校验会话验证码 
* 请求地址
    * GET|POST /verify/simg
* 参数说明
    * GET
        * t: 字符串，验证码类型，n - number（数字），s - string(字母), ns - number/string(字母+数字)，必选
        * l: 整数，验证码长度，必选
        * w: 整数，图片宽度，必选
        * h: 整数，图片高度，必选
        * f: 字符串，验证码字号数字，用','分隔，例如 f=32,43,23，必选
    * POST
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

## 获取和校验通用短信验证码
* 接口说明
    * 获取和校验短信验证码 
    * 验证码为数字
* 请求地址
    * GET|POST /verify/gsms
* 参数说明
    * GET
        * p: 字符串，手机号，必选
        * c: 字符串，用户输入的图片验证码，必选
        * v: 字符串，发送短信的图片验证码ID，必选
        * t: 字符串，发送短信验证码的短信模板标识，必选
        * l: 整数，短信验证码长度，必选
    * POST
        * p: 字符串，手机号，必选
        * c: 字符串，用户输入的验证码，必选
* 成功返回
    * GET
    ```
        成功：
        {
            "status": 0,
            "msg": "success",
            "data": {
                "expires": 360
            }
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

## 获取和校验用户短信验证码
* 接口说明
    * 获取和校验登录用户的短信验证码 
    * 验证码为数字
* 请求地址
    * GET|POST /verify/usms
* 参数说明
    * GET
        * t: 字符串，发送短信验证码的短信模板标识，必选
        * l: 整数，短信验证码长度，必选
    * POST
        * c: 字符串，用户输入的验证码，必选
* 接口返回
    * GET
    ```
        成功：
        {
            "status": 0,
            "msg": "success",
            "data": {
                "expires": 360
            }
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


## 查询Redis
* 接口说明
    * 查询指定的redis
* 请求地址
    * GET /admin/redis/get
* 参数说明
    * db: 整数，redis DB号
    * t: 字符串，redis存储类型，None-string, h-hash, l-list, s-set, z-sorted set
    * n: 字符串，redis键值名称，必选
* 接口返回
    * 成功
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
    * 失败
    ```
        {
            "status": -1221,
            "msg": "查询健值不存在",
            "data": null
        }
    ```

    
* 接口示例


## 删除Redis
* 接口说明
    * 清除指定的redis
    
* 请求地址
    * GET /admin/redis/del
* 参数说明
    * db: 整数，redis DB号
    * n: 字符串，redis键值名称，必选
* 接口返回
    * 成功
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: data
        }
    ```
    * 失败
    ```
        {
            "status": -1220,
            "msg": "查询DB不存在",
            "data": null
        }
    ```
* 接口示例

