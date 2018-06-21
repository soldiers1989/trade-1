"""
    query option for tdx
"""

# 股票行情查询
class gphq:
    zqdm = "zqdm" # 证券代码
    zqmc = "zqmc" # 证券名称

    zsj = "zsj" # 昨收盘价
    jkj = "jkj" # 今开盘价
    dqj = "dqj" # 当前价格

    zgj = "zgj" # 最高价格
    zdj = "zdj" # 最低价格

    np = "np" # 内盘，手
    wp = "wp" # 外盘，手

    cjl = "cjl" # 成交数量，手
    cje = "cje" # 成交金额


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
        zqdm: ["代码"],
        zqmc: ["名称"],

        zsj: ["昨收"],
        jkj: ["开盘"],
        dqj: ["现价"],

        zgj: ["最高价"],
        zdj: ["最低价"],

        np: ["内盘"],
        wp: ["外盘"],

        cjl: ["总量"],
        cje: ["总金额"],

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
