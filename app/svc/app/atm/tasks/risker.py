"""
    user trade risk manage
"""
import time, decimal
from .. import remote


def _money(val):
    """
        convert to money value
    :param val: str/decimal/number
    :return:
    """
    return decimal.Decimal(val).quantize(decimal.Decimal('.00'))


def check(*args, **kwargs):
    """
        risk checking for user hold trade list
        kwargs:
        {
            "config":{
                "rpc": {
                    "aam": {
                        "baseurl": "http://localhost:9001",
                        "key": "abc",
                        "safety": false
                    },
                    "mds": {
                        "baseurl": "http://localhost:10003",
                        "key": "abc",
                        "safety": false
                    }
                }
            },
            "callback": ""
        }
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        rpcmds = remote.tms.Mds(config['rpc']['mds']['baseurl'], config['rpc']['mds'].get('key'), config['rpc']['mds'].get('safety', False))

        # get user trade list
        usertrades = rpcaam.trade_risk_holds()

        # stocks of user trade
        stocks = set([item['scode'] for item in usertrades])

        # get current quote of stocks
        quotes = {}
        batches, counter, batch_limit = [], 0, 10
        for stock in stocks:
            if counter < batch_limit:
                batches.append(stock)
                counter += 1
                continue
            # fetch current quote of batch stocks
            zqdms = ','.join(batches)
            quotelst = rpcmds.stock_quote(zqdm=zqdms)

            # save quotes
            for q in quotelst:
                quotes[q['zqdm']] = q

            # clear current batch
            batches, counter = [], 0

        if len(batches) > 0:
            # fetch current quote of batch stocks
            zqdms = ','.join(batches)
            quotelst = rpcmds.stock_quote(zqdm=zqdms)

            # save quotes
            for q in quotelst:
                quotes[q['zqdm']] = q

        warning, stoploss, normal = [], [], []
        # compute user trade capital & market value
        for usertrade in usertrades:
            dqj = _money(quotes[usertrade['scode']]['dqj'])
            usertrade['capital'] = str(_money(_money(usertrade['bprice'])*_money(usertrade['bcount']))) # original capital
            usertrade['marketw'] = str(_money(_money(usertrade['capital']) * decimal.Decimal(usertrade['wline']))) # warning market value
            usertrade['markets'] = str(_money(_money(usertrade['capital']) * decimal.Decimal(usertrade['sline']))) # stop loss market value
            usertrade['marketv'] = str(_money(_money(usertrade['hcount'])*dqj + _money(usertrade['sprice'])*_money(usertrade['scount']) + _money(usertrade['amargin']))) # current market value
            usertrade['dqj'] = str(dqj)
            usertrade['rtime'] = int(time.time()) # risk fresh time

            if decimal.Decimal(usertrade['marketv']) < decimal.Decimal(usertrade['markets']):
                usertrade['risk'] = 'stoploss'
                stoploss.append(usertrade)
            elif decimal.Decimal(usertrade['marketv']) < decimal.Decimal(usertrade['marketw']):
                usertrade['risk'] = 'warning'
                warning.append(usertrade)
            else:
                usertrade['risk'] = 'normal'
                normal.append(usertrade)

        # update rick data
        rpcaam.trade_risk_set('warning', warning)
        rpcaam.trade_risk_set('stoploss', stoploss)
        rpcaam.trade_risk_set('normal', normal)

        swarning, sstoploss, snormal = [str(item) for item in warning], [str(item) for item in stoploss], [str(item) for item in normal]
        return '\nrisk-check: \nwarning:\n%s\nstoploss:\n%s\nnormal:\n%s\n' % ('\n'.join(swarning), '\n'.join(sstoploss), '\n'.join(snormal))
    except Exception as e:
        raise RuntimeError('risk-check: %s'%str(e))

