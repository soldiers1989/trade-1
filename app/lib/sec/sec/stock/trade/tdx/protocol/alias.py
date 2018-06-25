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
    for k, v in aliasobj.items():
        inverted['v'] = k

    return inverted


# 当前资产查询
dqzc = {
    'zzc': ["总资产"],
    'zjye': ["资金余额"],
    'kyzj': ["可用资金"],
    'kqzj': ["可取资金"],
    'djzj': ["冻结资金"],
    'zxsz': ["最新市值"],
    'fdyk': ["参考浮动盈亏"]
}
idqzc = invert(dqzc)


# 当前持仓查询
dqcc = {
    'zqdm': ["证券代码"],
    'zqmc': ["证券名称"],
    'zqsl': ["证券数量"],
    'kmsl': ["可卖数量"],
    'ckcb': ["参考成本价","摊薄成本价"],
    'mrjj': ["买入均价"],
    'dqj': ["当前价"],
    'zxsz': ["最新市值"],
    'fdyk': ["参考浮动盈亏","摊薄浮动盈亏"],
    'ykbl': ["盈亏比例(%)","参考盈亏比例(%)"],
    'gddm': ["股东代码"],
    'jysdm': ["交易所代码"]
}
idqcc = invert(dqcc)


# 当日委托查询
drwt = {
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
idrwt = invert(drwt)


# 当日成交查询
drcj = {
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
idrcj = invert(drcj)


# 可撤委托查询
kcwt = {
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
ikcwt = invert(kcwt)


# 股东信息查询
gdxx = {
    'gddm': ["股东代码"],
    'gdlx': ["股东类型"]
}
igdxx = invert(gdxx)


# 历史委托查询
lswt = {
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
ilswt = invert(lswt)

# 历史成交查询
lscj = {
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
ilscj = invert(lscj)


# 交割单查询
jgd = {
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
ijgd = invert(jgd)


# 股票行情查询
gphq = {
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
igphq = invert(gphq)


# 限价买入
xjmr = {
    'wtbh': ["委托编号"]
}
ixjmr = invert(xjmr)


# 限价卖出
xjmc = {
    'wtbh': ["委托编号"]
}
ixjmc = invert(xjmc)


# 市价买入
sjmr = {
    'wtbh': ["委托编号"]
}
isjmr = invert(sjmr)


# 市价卖出
sjmc = {
    'wtbh': ["委托编号"]
}
isjmc = invert(sjmc)


# 委托撤单
wtcd = {
    'wtbh': ["委托编号"]
}
iwtcd = invert(wtcd)
