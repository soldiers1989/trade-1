"""
    alias for tdx agent response
"""
from .. import norm

# 当前资产查询
_dqzc = {
    norm.dqzc.zzc: ["总资产"],
    norm.dqzc.zjye: ["资金余额"],
    norm.dqzc.kyzj: ["可用资金"],
    norm.dqzc.kqzj: ["可取资金"]
}

# 当前持仓查询
_dqcc = {
    norm.dqcc.zqdm: ["证券代码"],
    norm.dqcc.zqmc: ["证券名称"],
    norm.dqcc.zqsl: ["证券数量"],
    norm.dqcc.kmsl: ["可卖数量"]
}

# 当日委托查询
_drwt = {
    norm.drwt.wtrq: ["委托日期"],
    norm.drwt.wtsj: ["委托时间"],
    norm.drwt.gddm: ["股东代码"],
    norm.drwt.zqdm: ["证券代码"],
    norm.drwt.zqmc: ["证券名称"],
    norm.drwt.mmbz: ["买卖标志"],
    norm.drwt.wtjg: ["委托价格"],
    norm.drwt.wtsl: ["委托数量"],
    norm.drwt.wtbh: ["委托编号"],
    norm.drwt.cjsl: ["成交数量"],
    norm.drwt.cjjg: ["成交价格"],
    norm.drwt.cjje: ["成交金额"],
    norm.drwt.cdsl: ["撤单数量"],
    norm.drwt.cdbz: ["撤单标志","可撤单标志"],
    norm.drwt.ztsm: ["状态说明"]
}

# 当日成交查询
_drcj = {
    norm.drcj.cjrq: ["成交日期"],
    norm.drcj.cjsj: ["成交时间"],
    norm.drcj.gddm: ["股东代码"],
    norm.drcj.zqdm: ["证券代码"],
    norm.drcj.zqmc: ["证券名称"],
    norm.drcj.mmbz: ["买卖标志"],
    norm.drcj.wtjg: ["委托价格"],
    norm.drcj.wtsl: ["委托数量"],
    norm.drcj.wtbh: ["委托编号"],
    norm.drcj.cjsl: ["成交数量"],
    norm.drcj.cjjg: ["成交价格"],
    norm.drcj.cjje: ["成交金额","发生金额"],
    norm.drcj.cjbh: ["成交编号"],
    norm.drcj.cdbz: ["撤单标志"],
    norm.drcj.ztsm: ["状态说明"]
}

# 可撤委托查询
_kcwt = {
    norm.kcwt.wtrq: ["委托日期"],
    norm.kcwt.wtsj: ["委托时间"],
    norm.kcwt.gddm: ["股东代码"],
    norm.kcwt.zqdm: ["证券代码"],
    norm.kcwt.zqmc: ["证券名称"],
    norm.kcwt.mmbz: ["买卖标志"],
    norm.kcwt.wtjg: ["委托价格"],
    norm.kcwt.wtsl: ["委托数量"],
    norm.kcwt.wtbh: ["委托编号"],
    norm.kcwt.cjsl: ["成交数量"],
    norm.kcwt.cjjg: ["成交价格"],
    norm.kcwt.cjje: ["成交金额"],
    norm.kcwt.cdsl: ["撤单数量"],
    norm.kcwt.cdbz: ["撤单标志","可撤单标志"],
    norm.kcwt.ztsm: ["状态说明"]
}

# 股东信息查询
_gdxx = {
    norm.gdxx.gddm: ["股东代码"],
    norm.gdxx.gdmc: ["股东名称"],
    norm.gdxx.zjzh: ["资金账号"],
    norm.gdxx.gdlx: ["股东类型","账号类别"]
}


# 历史委托查询
_lswt = {
    norm.lswt.wtrq: ["委托日期"],
    norm.lswt.wtsj: ["委托时间"],
    norm.lswt.gddm: ["股东代码"],
    norm.lswt.zqdm: ["证券代码"],
    norm.lswt.zqmc: ["证券名称"],
    norm.lswt.mmbz: ["买卖标志"],
    norm.lswt.wtjg: ["委托价格"],
    norm.lswt.wtsl: ["委托数量"],
    norm.lswt.wtbh: ["委托编号"],
    norm.lswt.cjsl: ["成交数量"],
    norm.lswt.cjjg: ["成交价格"],
    norm.lswt.cjje: ["成交金额"],
    norm.lswt.cdsl: ["撤单数量"],
    norm.lswt.cdbz: ["撤单标志","可撤单标志"],
    norm.lswt.ztsm: ["状态说明"]
}

# 历史成交查询
_lscj = {
    norm.lscj.cjrq: ["成交日期"],
    norm.lscj.cjsj: ["成交时间"],
    norm.lscj.gddm: ["股东代码"],
    norm.lscj.zqdm: ["证券代码"],
    norm.lscj.zqmc: ["证券名称"],
    norm.lscj.mmbz: ["买卖标志"],
    norm.lscj.wtjg: ["委托价格"],
    norm.lscj.wtsl: ["委托数量"],
    norm.lscj.wtbh: ["委托编号"],
    norm.lscj.cjsl: ["成交数量"],
    norm.lscj.cjjg: ["成交价格"],
    norm.lscj.cjje: ["成交金额","发生金额"],
    norm.lscj.cjbh: ["成交编号"],
    norm.lscj.cdbz: ["撤单标志"],
    norm.lscj.ztsm: ["状态说明"]
}

# 交割单查询
_jgd = {
    norm.jgd.cjrq: ["成交日期"],
    norm.jgd.cjsj: ["成交时间"],
    norm.jgd.gddm: ["股东代码"],
    norm.jgd.zqdm: ["证券代码"],
    norm.jgd.zqmc: ["证券名称"],
    norm.jgd.mmbz: ["买卖标志"],
    norm.jgd.wtjg: ["委托价格"],
    norm.jgd.wtsl: ["委托数量"],
    norm.jgd.wtbh: ["委托编号"],
    norm.jgd.cjsl: ["成交数量"],
    norm.jgd.cjjg: ["成交价格"],
    norm.jgd.cjje: ["成交金额","发生金额"],
    norm.jgd.cjbh: ["成交编号"],
    norm.jgd.yj: ["佣金", "净佣金"],
    norm.jgd.yhs: ["印花税"],
    norm.jgd.ghf: ["过户费"],
    norm.jgd.jygf: ["交易规费"],
    norm.jgd.qtfy: ["其它费用","前台费用"]
}

# 股票行情查询
_gphq = {
    norm.gphq.zqdm: ["证券代码"],
    norm.gphq.zqmc: ["证券名称"],

    norm.gphq.zsj: ["昨收价"],
    norm.gphq.jkj: ["今开价"],
    norm.gphq.dqj: ["当前价"],

    norm.gphq.mrj1: ["买一价"],
    norm.gphq.mrj2: ["买二价"],
    norm.gphq.mrj3: ["买三价"],
    norm.gphq.mrj4: ["买四价"],
    norm.gphq.mrj5: ["买五价"],

    norm.gphq.mrl1: ["买一量"],
    norm.gphq.mrl2: ["买二量"],
    norm.gphq.mrl3: ["买三量"],
    norm.gphq.mrl4: ["买四量"],
    norm.gphq.mrl5: ["买五量"],

    norm.gphq.mcj1: ["卖一价"],
    norm.gphq.mcj2: ["卖二价"],
    norm.gphq.mcj3: ["卖三价"],
    norm.gphq.mcj4: ["卖四价"],
    norm.gphq.mcj5: ["卖五价"],

    norm.gphq.mcl1: ["卖一量"],
    norm.gphq.mcl2: ["卖二量"],
    norm.gphq.mcl3: ["卖三量"],
    norm.gphq.mcl4: ["卖四量"],
    norm.gphq.mcl5: ["卖五量"]
}

# 委托下单
_wtxd = {
    norm.wtxd.wtbh: ["委托编号"]
}

# 委托撤单
_wtcd = {
    norm.wtcd.cdxx: ["委托编号"]
}


query = {
    'dqzc': norm.invert(_dqzc),
    'dqcc': norm.invert(_dqcc),
    'drwt': norm.invert(_drwt),
    'drcj': norm.invert(_drcj),
    'kcwt': norm.invert(_kcwt),
    'gdxx': norm.invert(_gdxx),
    'lswt': norm.invert(_lswt),
    'lscj': norm.invert(_lscj),
    'jgd': norm.invert(_jgd)
}

gphq = norm.invert(_gphq)
wtxd = norm.invert(_wtxd)
wtcd = norm.invert(_wtcd)