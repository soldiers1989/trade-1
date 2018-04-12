"""
    option for tdx interface
"""

# 当前资产查询
class dqzc:
    type = "0"

    zzc = "zzc"
    zjye = "zjye"
    kyzj = "kyzj"
    kqzj = "kqzj"
    djzj = "djzj"
    zxsz = "zxsz"
    fdyk = "fdyk"

    alias = {
        zzc: ["总资产"],
        zjye: ["资金余额"],
        kyzj: ["可用资金"],
        kqzj: ["可取资金"],
        djzj: ["冻结资金"],
        zxsz: ["最新市值"],
        fdyk: ["参考浮动盈亏"]
    }

# 当前持仓查询
class dqcc:
    type = "1"

    zqdm = "zqdm"
    zqmc = "zqmc"
    zqsl = "zqsl"
    kmsl = "kmsl"
    ckcb = "ckcb"
    mrjj = "mrjj"
    dqj = "dqj"
    zxsz = "zxsz"
    fdyk = "fdyk"
    ykbl = "ykbl"
    gddm = "gddm"
    jysdm = "jysdm"

    alias = {
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        zqsl: ["证券数量"],
        kmsl: ["可卖数量"],
        ckcb: ["参考成本价","摊薄成本价"],
        mrjj: ["买入均价"],
        dqj: ["当前价"],
        zxsz: ["最新市值"],
        fdyk: ["参考浮动盈亏","摊薄浮动盈亏"],
        ykbl: ["盈亏比例(%)","参考盈亏比例(%)"],
        gddm: ["股东代码"],
        jysdm: ["交易所代码"]
    }

# 当日委托查询
class drwt:
    type = "2"

    wtrq = "wtrq"
    wtsj = "wtsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cdsl = "cdsl"
    cdbz = "cdbz"
    ztsm = "ztsm"

    alias = {
        wtrq: ["委托日期"],
        wtsj: ["委托时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额"],
        cdsl: ["撤单数量"],
        cdbz: ["撤单标志","可撤单标志"],
        ztsm: ["状态说明"]
    }


# 当日成交查询
class drcj:
    type = "3"

    cjrq = "cjrq"
    cjsj = "cjsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cjbh = "cjbh"
    cdbz = "cdbz"
    ztsm = "ztsm"

    alias = {
        cjrq: ["成交日期"],
        cjsj: ["成交时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额","发生金额"],
        cjbh: ["成交编号"],
        cdbz: ["撤单标志"],
        ztsm: ["状态说明"]
    }


# 可撤委托查询
class kcwt:
    type = "4"

    wtrq = "wtrq"
    wtsj = "wtsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cdsl = "cdsl"
    cdbz = "cdbz"
    ztsm = "ztsm"

    alias = {
        wtrq: ["委托日期"],
        wtsj: ["委托时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额"],
        cdsl: ["撤单数量"],
        cdbz: ["撤单标志","可撤单标志"],
        ztsm: ["状态说明"]
    }

# 股东信息查询
class gdxx:
    type = "5"

    gddm = "gddm"
    gdlx = "gdlx"

    alias = {
        gddm: ["股东代码"],
        gdlx: ["股东类型"]
    }


# 历史委托查询
class lswt:
    type = "0"

    wtrq = "wtrq"
    wtsj = "wtsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cdsl = "cdsl"
    cdbz = "cdbz"
    ztsm = "ztsm"

    alias = {
        wtrq: ["委托日期"],
        wtsj: ["委托时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额"],
        cdsl: ["撤单数量"],
        cdbz: ["撤单标志","可撤单标志"],
        ztsm: ["状态说明"]
    }

# 历史成交查询
class lscj:
    type = "1"

    cjrq = "cjrq"
    cjsj = "cjsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cjbh = "cjbh"
    cdbz = "cdbz"
    ztsm = "ztsm"

    alias = {
        cjrq: ["成交日期"],
        cjsj: ["成交时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额","发生金额"],
        cjbh: ["成交编号"],
        cdbz: ["撤单标志"],
        ztsm: ["状态说明"]
    }

# 交割单查询
class jgd:
    type = "3"

    cjrq = "cjrq"
    cjsj = "cjsj"
    gddm = "gddm"
    zqdm = "zqdm"
    zqmc = "zqmc"
    mmbz = "mmbz"
    wtjg = "wtjg"
    wtsl = "wtsl"
    wtbh = "wtbh"
    cjsl = "cjsl"
    cjjg = "cjjg"
    cjje = "cjje"
    cjbh = "cjbh"
    yj = "yj"
    yhs = "yhs"
    ghf = "ghf"
    jygf = "jygf"
    qtfy = "qtfy"


    alias = {
        cjrq: ["成交日期"],
        cjsj: ["成交时间"],
        gddm: ["股东代码"],
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],
        mmbz: ["买卖标志"],
        wtjg: ["委托价格"],
        wtsl: ["委托数量"],
        wtbh: ["委托编号"],
        cjsl: ["成交数量"],
        cjjg: ["成交价格"],
        cjje: ["成交金额","发生金额"],
        cjbh: ["成交编号"],
        yj: ["佣金", "净佣金"],
        yhs: ["印花税"],
        ghf: ["过户费"],
        jygf: ["交易规费"],
        qtfy: ["其它费用","前台费用"]
    }

# 股票行情查询
class gphq:
    zqdm = "zqdm"
    zqmc = "zqmc"

    zsj = "zsj"
    jkj = "jkj"
    dqj = "dqj"

    mrj1 = "mrj1"
    mrj2 = "mrj2"
    mrj3 = "mrj3"
    mrj4 = "mrj4"
    mrj5 = "mrj5"

    mrl1 = "mrl1"
    mrl2 = "mrl2"
    mrl3 = "mrl3"
    mrl4 = "mrl4"
    mrl5 = "mrl5"

    mcj1 = "mcj1"
    mcj2 = "mcj2"
    mcj3 = "mcj3"
    mcj4 = "mcj4"
    mcj5 = "mcj5"

    mcl1 = "mcl1"
    mcl2 = "mcl2"
    mcl3 = "mcl3"
    mcl4 = "mcl4"
    mcl5 = "mcl5"

    alias = {
        zqdm: ["证券代码"],
        zqmc: ["证券名称"],

        zsj: ["昨收价"],
        jkj: ["今开价"],
        dqj: ["当前价"],

        mrj1: ["买一价"],
        mrj2: ["买二价"],
        mrj3: ["买三价"],
        mrj4: ["买四价"],
        mrj5: ["买五价"],

        mrl1: ["买一量"],
        mrl2: ["买二量"],
        mrl3: ["买三量"],
        mrl4: ["买四量"],
        mrl5: ["买五量"],

        mcj1: ["卖一价"],
        mcj2: ["卖二价"],
        mcj3: ["卖三价"],
        mcj4: ["卖四价"],
        mcj5: ["卖五价"],

        mcl1: ["卖一量"],
        mcl2: ["卖二量"],
        mcl3: ["卖三量"],
        mcl4: ["卖四量"],
        mcl5: ["卖五量"]
    }

# 限价买入
class xjmr:
    otype = "0" # 买入
    ptype = "0" # 限价

    wtbh = "wtbh"

    alias = {
        wtbh: ["委托编号"]
    }

# 限价卖出
class xjmc:
    otype = "1" # 卖出
    ptype = "0" # 限价

    wtbh = "wtbh"

    alias = {
        wtbh: ["委托编号"]
    }

# 市价买入
class sjmr:
    otype = "0" # 买入
    ptype = "1" # 市价

    wtbh = "wtbh"

    alias = {
        wtbh: ["委托编号"]
    }

# 市价卖出
class sjmc:
    otype = "1" # 卖出
    ptype = "1" # 市价

    wtbh = "wtbh"

    alias = {
        wtbh: ["委托编号"]
    }

# 委托撤单
class wtcd:
    wtbh = "wtbh"

    alias = {
        wtbh: ["委托编号"]
    }
