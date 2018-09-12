"""
    alias for tdx agent response
"""


# invert of alias
def invert(aliasobj):
    """
        invert
    :param obj:
    :return:
    """
    inverted = {}
    for alias, names in aliasobj.items():
        for name in names:
            inverted[name] = alias

    return inverted


# 当前资产查询
_DQZC = {
    'zzc': ["总资产"],
    'zjye': ["资金余额"],
    'kyzj': ["可用资金"],
    'kqzj': ["可取资金"]
}
dqzc = invert(_DQZC)


# 当前持仓查询
_DQCC = {
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'zqsl': ["证券数量"],
    'kmsl': ["可卖数量"]
}
dqcc = invert(_DQCC)


# 当日委托查询
_DRWT = {
    'wtrq': ["委托日期"],
    'wtsj': ["委托时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'mmbz': ["买卖标志"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cjjg': ["成交价格"],
    'cjje': ["成交金额"],
    'cdsl': ["撤单数量"],
    'cdbz': ["撤单标志","可撤单标志"],
    'ztsm': ["状态说明"]
}
drwt = invert(_DRWT)


# 当日成交查询
_DRCJ = {
    'cjrq': ["成交日期"],
    'cjsj': ["成交时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'mmbz': ["买卖标志"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cjjg': ["成交价格"],
    'cjje': ["成交金额","发生金额"],
    'cjbh': ["成交编号"],
    'cdbz': ["撤单标志"],
    'ztsm': ["状态说明"]
}
drcj = invert(_DRCJ)


# 可撤委托查询
_KCWT = {
    'wtrq': ["委托日期"],
    'wtsj': ["委托时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cdsl': ["撤单数量"],
    'ztsm': ["状态说明"]
}
kcwt = invert(_KCWT)


# 股东信息查询
_GDXX = {
    'gddm': ["股东代码"],
    'gdmc': ['股东名称'],
    'zjzh': ['资金账号'],
    'gdlx': ["股东类型","账号类别"]
}
gdxx = invert(_GDXX)


# 历史委托查询
_LSWT = {
    'wtrq': ["委托日期"],
    'wtsj': ["委托时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'mmbz': ["买卖标志"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cjjg': ["成交价格"],
    'cjje': ["成交金额"],
    'cdsl': ["撤单数量"],
    'cdbz': ["撤单标志","可撤单标志"],
    'ztsm': ["状态说明"]
}
lswt = invert(_LSWT)


# 历史成交查询
_LSCJ = {
    'cjrq': ["成交日期"],
    'cjsj': ["成交时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'mmbz': ["买卖标志"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cjjg': ["成交价格"],
    'cjje': ["成交金额","发生金额"],
    'cjbh': ["成交编号"]
}
lscj = invert(_LSCJ)


# 交割单查询
_JGD = {
    'cjrq': ["成交日期"],
    'cjsj': ["成交时间"],
    'gddm': ["股东代码"],
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'mmbz': ["买卖标志"],
    'wtjg': ["委托价格"],
    'wtsl': ["委托数量"],
    'wtbh': ["委托编号"],
    'cjsl': ["成交数量"],
    'cjjg': ["成交价格"],
    'cjje': ["成交金额","发生金额"],
    'cjbh': ["成交编号"],
    'yj': ["佣金", "净佣金"],
    'yhs': ["印花税"],
    'ghf': ["过户费"],
    'jygf': ["交易规费"],
    'qtfy': ["其它费用","前台费用"]
}
jgd = invert(_JGD)


# 股票行情查询
_GPHQ = {
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],

    'zsj': ["昨收价"],
    'jkj': ["今开价"],
    'dqj': ["当前价"],

    'mrj1': ["买一价"],
    'mrj2': ["买二价"],
    'mrj3': ["买三价"],
    'mrj4': ["买四价"],
    'mrj5': ["买五价"],

    'mrl1': ["买一量"],
    'mrl2': ["买二量"],
    'mrl3': ["买三量"],
    'mrl4': ["买四量"],
    'mrl5': ["买五量"],

    'mcj1': ["卖一价"],
    'mcj2': ["卖二价"],
    'mcj3': ["卖三价"],
    'mcj4': ["卖四价"],
    'mcj5': ["卖五价"],

    'mcl1': ["卖一量"],
    'mcl2': ["卖二量"],
    'mcl3': ["卖三量"],
    'mcl4': ["卖四量"],
    'mcl5': ["卖五量"]
}
gphq = invert(_GPHQ)


# 限价买入
_XJMR = {
    'wtbh': ["委托编号"]
}
xjmr = invert(_XJMR)


# 限价卖出
_XJMC = {
    'wtbh': ["委托编号"]
}
xjmc = invert(_XJMC)


# 市价买入
_SJMR = {
    'wtbh': ["委托编号"]
}
sjmr = invert(_SJMR)


# 市价卖出
_SJMC = {
    'wtbh': ["委托编号"]
}
sjmc = invert(_SJMC)


# 委托撤单
_WTCD = {
    'fhxx': ["返回信息"]
}
wtcd = invert(_WTCD)
