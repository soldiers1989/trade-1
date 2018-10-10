"""
    protocol response data normalize definition
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
class dqzc:
    zzc='zzc' #"总资产"
    zjye='zjye' #"资金余额"
    kyzj='kyzj' #"可用资金"
    kqzj='kqzj' #"可取资金"


# 当前持仓查询
class dqcc:
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    zqsl='zqsl' #"证券数量"
    kmsl='kmsl' #"可卖数量"


# 当日委托查询
class drwt:
    wtrq='wtrq' #"委托日期"
    wtsj='wtsj' #"委托时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额"
    cdsl='cdsl' #"撤单数量"
    cdbz='cdbz' #"撤单标志","可撤单标志"
    ztsm='ztsm' #"状态说明"


# 当日成交查询
class drcj:
    cjrq='cjrq' #"成交日期"
    cjsj='cjsj' #"成交时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额","发生金额"
    cjbh='cjbh' #"成交编号"
    cdbz='cdbz' #"撤单标志"
    ztsm='ztsm' #"状态说明"]


# 可撤委托查询
class kcwt:
    wtrq='wtrq' #"委托日期"
    wtsj='wtsj' #"委托时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额"
    cdsl='cdsl' #"撤单数量"
    cdbz='cdbz' #"撤单标志","可撤单标志"
    ztsm='ztsm' #"状态说明"


# 股东信息查询
class gdxx:
    gddm='gddm' #"股东代码"
    gdmc='gdmc' # 股东名称
    zjzh='zjzh' # 资金账号
    gdlx='gdlx' #"股东类型","账号类别"


# 历史委托查询
class lswt:
    wtrq='wtrq' #"委托日期"
    wtsj='wtsj' #"委托时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额"
    cdsl='cdsl' #"撤单数量"
    cdbz='cdbz' #"撤单标志","可撤单标志"
    ztsm='ztsm' #"状态说明"


# 历史成交查询
class lscj:
    cjrq='cjrq' #"成交日期"
    cjsj='cjsj' #"成交时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额","发生金额"
    cjbh='cjbh' #"成交编号"
    cdbz='cdbz' #"撤单标志"
    ztsm='ztsm' #"状态说明"


# 交割单查询
class jgd:
    cjrq='cjrq' #"成交日期"
    cjsj='cjsj' #"成交时间"
    gddm='gddm' #"股东代码"
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"
    mmbz='mmbz' #"买卖标志"
    wtjg='wtjg' #"委托价格"
    wtsl='wtsl' #"委托数量"
    wtbh='wtbh' #"委托编号"
    cjsl='cjsl' #"成交数量"
    cjjg='cjjg' #"成交价格"
    cjje='cjje' #"成交金额","发生金额"
    cjbh='cjbh' #"成交编号"
    yj='yj' #"佣金", "净佣金"
    yhs='yhs' #"印花税"
    ghf='ghf' #"过户费"
    jygf='jygf' #"交易规费"
    qtfy='qtfy' #"其它费用","前台费用"


# 股票行情查询
class gphq:
    zqdm='zqdm' #"证券代码"
    zqmc='zqmc' #"证券名称"

    zsj='zsj' #"昨收价"
    jkj='jkj' #"今开价"
    dqj='dqj' #"当前价"

    mrj1='mrj1' #"买一价"
    mrj2='mrj2' #"买二价"
    mrj3='mrj3' #"买三价"
    mrj4='mrj4' #"买四价"
    mrj5='mrj5' #"买五价"

    mrl1='mrl1' #"买一量"
    mrl2='mrl2' #"买二量"
    mrl3='mrl3' #"买三量"
    mrl4='mrl4' #"买四量"
    mrl5='mrl5' #"买五量"

    mcj1='mcj1' #"卖一价"
    mcj2='mcj2' #"卖二价"
    mcj3='mcj3' #"卖三价"
    mcj4='mcj4' #"卖四价"
    mcj5='mcj5' #"卖五价"

    mcl1='mcl1' #"卖一量"
    mcl2='mcl2' #"卖二量"
    mcl3='mcl3' #"卖三量"
    mcl4='mcl4' #"卖四量"
    mcl5='mcl5' #"卖五量"


# 委托下单
class wtxd:
    wtbh='wtbh' #"委托编号"


# 委托撤单
class wtcd:
    cdxx='cdxx' #"撤单信息"
