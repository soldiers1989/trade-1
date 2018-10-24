import tushare

if __name__ == '__main__':
    result = tushare.get_today_ticks('000001')
    print(result)