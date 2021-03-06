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


## 修改密码
* 接口说明
    * 验证旧密码，修改为新密码
* 请求地址
    * POST /user/cpwd
* 参数说明
    * opwd: 字符串，旧密码，必选
    * npwd: 字符串, 新密码, 必选
* 响应格式
    * 成功
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
    * 失败
    ```
        {
            "status": -1005,
            "msg": "原始密码错误",
            "data": null
        }
            
    ```
* 接口示例

## 找回密码
* 接口说明
    * 输入手机号、验证码，重新设置密码
* 请求地址
    * POST /user/fpwd
* 参数说明
    * phone: 字符串，注册手机号，必选
    * npwd: 字符串, 新密码, 必选
    * vcode: 字符串，手机验证码，必选
* 响应格式
    * 成功
    ```
        {
            “status”: 0,
            “msg”: ”success”,
            “data”: null
        }
    ```
    * 失败
    ```
        {
            "status": -1211,
            "msg": "短信验验码错误",
            "data": null
        }     
    ```
* 接口示例

## 获取用户银行卡
* 接口说明
    * 获取当前登录用户的银行卡列表
* 请求地址
    * POST /user/bank/get
* 参数说明
    * 无
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": [
                {
                    "id": 6,
                    "bank": "招商银行",
                    "name": "王五",
                    "account": "6112456614475878636457878",
                    "ctime": 1532057272,
                    "mtime": 1532057272,
                    "user": 4
                }
            ]
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 添加用户银行卡
* 接口说明
    * 添加当前登录用户银行卡
* 请求地址
    * POST /user/bank/add
* 参数说明
    * name: 字符串，开户人姓名，必选
    * idc: 字符串，开户人身份证号，必选
    * bank: 字符串，开户行名称，必选
    * account: 字符串，银行账号，必选
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": null
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 删除用户银行卡
* 接口说明
    * 添加当前登录用户银行卡
* 请求地址
    * POST /user/bank/del
* 参数说明
    * id: 数字，银行卡记录ID，必选
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": null
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 获取用户优惠券
* 接口说明
    * 获取当前登录用户的优惠券列表
* 请求地址
    * POST /user/coupon/get
* 参数说明
    * 无
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": [
                {
                    "id": 1,
                    "name": "赠送",
                    "money": "10.00",
                    "status": "unused",
                    "ctime": 1527261052,
                    "etime": 3055922104,
                    "utime": null,
                    "user": 1
                },
                {
                    "id": 2,
                    "name": "赠送",
                    "money": "10.00",
                    "status": "unused",
                    "ctime": 1527261052,
                    "etime": 3055922104,
                    "utime": null,
                    "user": 1
                }
            ]
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 获取用户资金流水明细
* 接口说明
    * 获取当前登录用户的资金流水明细列表
* 请求地址
    * POST /user/bill/get
* 参数说明
    * 无
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": [
                {
                    "id": 1,
                    "code": "000001",
                    "item": "充值",
                    "detail": "xxx充值",
                    "bmoney": "100.00",
                    "lmoney": "10000.00",
                    "ctime": 1527261052,
                    "user": 1
                },
                {
                    "id": 2,
                    "code": "000002",
                    "item": "提现",
                    "detail": "xxx提现",
                    "bmoney": "-100.00",
                    "lmoney": "9999.00",
                    "ctime": 1527261052,
                    "user": 1
                }
            ]
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 获取用户充值记录
* 接口说明
    * 获取当前登录用户的充值记录列表
* 请求地址
    * POST /user/charge/get
* 参数说明
    * 无
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": [
                {
                    "id": 1,
                    "code": "000001",
                    "money": "100.00",
                    "status": "topay",
                    "ctime": 1527261052,
                    "user": 1
                },
                {
                    "id": 2,
                    "code": "000002",
                    "money": "100.00",
                    "status": "topay",
                    "ctime": 1527261052,
                    "user": 1
                }
            ]
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
        }   
    ```
* 接口示例

## 获取用户提现记录
* 接口说明
    * 获取当前登录用户的提现记录列表
* 请求地址
    * POST /user/draw/get
* 参数说明
    * 无
* 响应格式
    * 成功
    ```
        {
            "status": 0,
            "msg": "success",
            "data": [
                {
                    "id": 1,
                    "code": "000001",
                    "money": "100.00",
                    "name": "张三",
                    "idc": "",
                    "bank": "中国银行",
                    "account": "212121112212",
                    "status": "paied",
                    "ctime": 1527261052,
                    "user": 1
                },
                {
                    "id": 2,
                    "code": "000002",
                    "money": "100.00",
                    "name": "张三",
                    "idc": "",
                    "bank": "中信银行",
                    "account": "54546456545646",
                    "status": "topay",
                    "ctime": 1527261052,
                    "user": 1
                }
            ]
        }
    ```
    * 失败
    ```
        {
            "status": -1000,
            "msg": "用户未登录",
            "data": null
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

