# 接口说明
* 接口通讯采用http协议，无状态请求/响应模式
* 请求为GET/POST方式
* 响应为JSON格式内容
    >成功：{“status”:0, “msg”:”status description”, “data”:json}

    >失败：{“status”:-1, “msg”:”status description”, “data”:json}
    
# 相关模块
## Pub模块

## quote模块
### 功能说明
    提供股票行情相关数据查询接口服务，包括股票五档行情等
    
### 接口设计
* 单个股票行情查询

* 批量股票行情查询

## trade模块