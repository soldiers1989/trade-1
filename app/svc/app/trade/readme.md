# 模块说明
    提供股票交易相关服务接口
    
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

## 账户登录
* 接口说明
    * 登录所有或者某个股票账户
* 请求地址
    * GET /login?account=$account
* 参数说明
    * account: 字符串，股票账户，可选
* 接口示例

## 账户登出
* 接口说明
    * 登出所有或者某个股票账户
* 请求地址
    * GET /logout?account=$account
* 参数说明
    * account: 字符串，股票账户，可选
* 接口示例

## 账户状态
* 接口说明
    * 查询所有或者某个股票账户当前状态
* 请求地址
    * GET /status?account=$account
* 参数说明
    * account: 字符串，股票账户，可选
* 接口示例

## 股票行情
* 接口说明
    * 查询某个股票当前五档行情
* 请求地址
    * GET /query/gphq?account=$account&code=$code
* 参数说明
    * account: 字符串，股票账户，必选
    * code: 字符串, 股票代码, 必选
* 接口示例

## 股东信息
* 接口说明
    * 查询某个股票账户的股东信息
* 请求地址
    * GET /query/gdxx?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 当前资产
* 接口说明
    * 查询某个股票账户的当前资产信息
* 请求地址
    * GET /query/dqzc?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 当前持仓
* 接口说明
    * 查询某个股票账户的当前持仓信息
* 请求地址
    * GET /query/dqcc?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 当日委托
* 接口说明
    * 查询某个股票账户的当日委托信息
* 请求地址
    * GET /query/drwt?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 当日成交
* 接口说明
    * 查询某个股票账户的当日成交信息
* 请求地址
    * GET /query/drcj?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 可撤委托
* 接口说明
    * 查询某个股票账户的当日可撤委托
* 请求地址
    * GET /query/kcwt?account=$account
* 参数说明
    * account: 字符串，股票账户，必选
* 接口示例

## 历史委托
* 接口说明
    * 查询某个股票账户的当日可撤委托
* 请求地址
    * GET /query/lswt?account=$account&sdate=$sdate&edate=$edate
* 参数说明
    * account: 字符串，股票账户，必选
    * sdate: 日期, 起始日期，格式：YYYYmmdd，必选
    * edate: 日期, 截止日期，格式：YYYYmmdd，必选
* 接口示例

## 历史委托
* 接口说明
    * 查询某个股票账户的历史成交信息
* 请求地址
    * GET /query/lscj?account=$account&sdate=$sdate&edate=$edate
* 参数说明
    * account: 字符串，股票账户，必选
    * sdate: 日期, 起始日期，格式：YYYYmmdd，必选
    * edate: 日期, 截止日期，格式：YYYYmmdd，必选
* 接口示例

## 交割单
* 接口说明
    * 查询某个股票账户的历史交割单信息
* 请求地址
    * GET /query/jgd?account=$account&sdate=$sdate&edate=$edate
* 参数说明
    * account: 字符串，股票账户，必选
    * sdate: 日期, 起始日期，格式：YYYYmmdd，必选
    * edate: 日期, 截止日期，格式：YYYYmmdd，必选
* 接口示例

## 限价买入
* 接口说明
    * 限价委托买入某只股票
* 请求地址
    * GET /order/xjmr?account=$account&gddm=$gddm&code=$code&price=$price&count=$count
* 参数说明
    * account: 字符串，股票账户，必选
    * gddm: 字符串, 交易所股东代码，与股票上市交易所对应，必选
    * code: 字符串, 股票代码，必选
    * price: 浮点数，委托价格，必选
    * count：整数，委托数量，100的整数倍，必选
* 接口示例

## 限价卖出
* 接口说明
    * 限价委托卖出某只股票
* 请求地址
    * GET /order/xjmc?account=$account&gddm=$gddm&code=$code&price=$price&count=$count
* 参数说明
    * account: 字符串，股票账户，必选
    * gddm: 字符串, 交易所股东代码，与股票上市交易所对应，必选
    * code: 字符串, 股票代码，必选
    * price: 浮点数，委托价格，必选
    * count：整数，委托数量，100的整数倍，必选
* 接口示例

## 市价买入
* 接口说明
    * 市价委托买入某只股票
* 请求地址
    * GET /order/sjmr?account=$account&gddm=$gddm&code=$code&price=$price&count=$count
* 参数说明
    * account: 字符串，股票账户，必选
    * gddm: 字符串, 交易所股东代码，与股票上市交易所对应，必选
    * code: 字符串, 股票代码，必选
    * price: 浮点数，委托价格，必选
    * count：整数，委托数量，100的整数倍，必选
* 接口示例

## 市价卖出
* 接口说明
    * 市价委托卖出某只股票
* 请求地址
    * GET /order/sjmc?account=$account&gddm=$gddm&code=$code&price=$price&count=$count
* 参数说明
    * account: 字符串，股票账户，必选
    * gddm: 字符串, 交易所股东代码，与股票上市交易所对应，必选
    * code: 字符串, 股票代码，必选
    * price: 浮点数，委托价格，必选
    * count：整数，委托数量，100的整数倍，必选
* 接口示例

## 撤销委托
* 接口说明
    * 撤销某个委托订单
* 请求地址
    * GET /order/cancel?account=$account&seid=$seid&code=$code
* 参数说明
    * account: 字符串，股票账户，必选
    * seid: 字符串, 股票所属交易所代码，0-深圳，1-上海，必选
    * code: 字符串, 股票代码，必选
* 接口示例