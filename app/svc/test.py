import tushare, pytdx.hq

if __name__ == '__main__':
    #result = tushare.get_hist_data('000001', ktype='5')
    #result = tushare.get_h_data('000001')
    tdxhq = pytdx.hq.TdxHq_API()
    tdxhq.connect("124.160.88.183", 7709)

    results = tdxhq.get_security_bars(0,0, '000001', 100, 5)
    print(results)