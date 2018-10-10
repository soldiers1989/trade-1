"""
    const variables for remote tdx agent
"""

# 查询账户数据
query = {
    "current": {
        "dqzc": "0", # 当前资产
        "dqcc": "1", # 当前持仓
        "drwt": "2", # 当日委托
        "drcj": "3", # 当日成交
        "kcwt": "4", # 可撤委托
        "gdxx": "5", # 股东信息
    },
    "history": {
        "lswt": "0", # 历史委托
        "lscj": "1", # 历史成交
        "jgd": "3" # 交割单
    }
}

# 委托买卖方向
otype = {
    "buy": "0",
    "sell": "1"
}

# 委托价格类型
ptype = {
    "xj": "0", # 限价
    "sj": "4" # 市价，五档即成剩余撤销
}
