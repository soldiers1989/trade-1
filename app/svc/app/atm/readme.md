# 模块说明
    后端定时任务服务管理和执行模块
   
# 依赖模块
* tlib
* trpc
* requests
* 

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