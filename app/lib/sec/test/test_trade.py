"""

"""
from sec.stock.trade import tdx, trades

if __name__ == '__main__':
    trds = trades.Trades()

    id = 'pollywang'
    acount = tdx.account.Account('030000012782','013579','030000012782','013579', '1', '7.38', [('agent1','172.16.21.135', 80)], [('trade1', '116.228.234.71', 7708)])
    #acount = tdx.account.Account('29633865', '456789', '29633865', '456789', '0', '7.16', [('agent1', '172.16.21.137', 81), ('agent2', '172.16.21.135', 80)], [('trade1', '117.40.3.6', 7708), ('trade2', '202.130.235.187', 7708)])
    #acount = tdx.account.Account('305000036', '133289', '305000036', '133289', '1', '6.10', [('agent1', '172.16.21.135', 80)], [('trade1', '117.40.3.6', 7708)])

    trds.add(id, acount)


    # 股东信息
    res = trds.query_gdxx(id)
    print(res)

    # 当前资产
    res = trds.query_dqzc(id)
    print(res)

    # 当前持仓
    res = trds.query_dqcc(id)
    print(res)

    # 当日成交
    res = trds.query_drcj(id)
    print(res)

    # 当日委托
    res = trds.query_drwt(id)
    print(res)

    # 可撤委托
    res = trds.query_kcwt(id)
    print(res)

    # 历史委托
    res = trds.query_lswt(id, '20180625', '20180626')
    print(res)

    # 历史成交
    res = trds.query_lscj(id, '20180625', '20180626')
    print(res)

    # 交割单
    res = trds.query_jgd(id, '20180625', '20180626')
    print(res)

    print(trds.status())

    #res = acount.logout()
    #print(res)