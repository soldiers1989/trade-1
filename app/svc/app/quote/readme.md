# 模块说明
    提供股票行情查询相关服务接口
    
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
    * 查询行情服务当前状态
* 请求地址
    * GET /status
* 参数说明
    * 无
* 接口示例

## 五档行情
* 接口说明
    * 查询某个或多个股票当前的五档行情
* 请求地址
    * GET /current?code=$code,$code,$code,...
* 参数说明
    * code: 字符串，股票代码，多个股票用','分割，必选
* 接口示例
