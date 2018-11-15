"""
    robot trade service for user trade order
"""
import datetime
from .. import remote


def take(*args, **kwargs):
    """
        take order from user
        kwargs:
        {
            config:{
                rpc: {
                    aam: {
                        baseurl: <baseurl>
                        key: <key>
                        safety: <True|False>
                    }
                }
            },
            callback: <url>
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

        # get user trade need to take
        usertrades = rpcaam.trade_list(status__in='tobuy,tosell,toclose,cancelbuy,cancelsell,cancelclose')

        taked, failed = [], []
        # process user trade
        for usertrade in usertrades:
            try:
                tradeid = usertrade['id']
                if usertrade['status'] in ['tobuy']:
                    rpcaam.trade_sys_buy(trade=tradeid)
                elif usertrade['status'] in ['tosell', 'toclose']:
                    rpcaam.trade_sys_sell(trade=tradeid)
                elif usertrade['status'] in ['cancelbuy', 'cancelsell', 'cancelclose']:
                    rpcaam.trade_sys_cancel(trade=tradeid)
                else:
                    pass
                taked.append(str(usertrade))
            except Exception as e:
                failed.append(str(usertrade)+", error: "+str(e))

        return '\ntrade(take): \ntaked:\n%s\nfailed:\n%s\n' % ('\n'.join(taked), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('trade(take): %s'%str(e))


def place(*args, **kwargs):
    """
        place order to trade account
        kwargs:
        {
            config:{
                rpc: {
                    aam: {
                        baseurl: <baseurl>
                        key: <key>
                        safety: <True|False>
                    }
                }
            },
            callback: <url>
        }
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

        # get user trade orders need to place
        tradeorders = rpcaam.trade_order_list(status__in='tosend,tocancel')

        placed, failed = [], []
        # process user trade orders
        for tradeorder in tradeorders:
            try:
                if tradeorder['status'] == 'tosend':
                    # update trade order status from tosend->sent
                    rpcaam.trade_order_sent(id=tradeorder['id'])
                    # place order to account
                    rpcaam.order_place(**tradeorder)
                elif  tradeorder['status'] == 'tocancel':
                    # update trade order status from tocancel->canceling
                    rpcaam.trade_order_canceling(id=tradeorder['id'])
                    # cancel order to account
                    rpcaam.order_cancel(ocode=tradeorder['ocode'])
                else:
                    pass
                placed.append(str(tradeorder))
            except Exception as e:
                failed.append(str(tradeorder)+", error: "+str(e))

        return '\ntrade(place): \nplaced:\n%s\nfailed:\n%s\n' % ('\n'.join(placed), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('trade(place): %s'%str(e))


def notify(*args, **kwargs):
    """
        notify order result to user
        kwargs:
        {
            config:{
                rpc: {
                    aam: {
                        baseurl: <baseurl>
                        key: <key>
                        safety: <True|False>
                    }
                }
            },
            callback: <url>
        }
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

        # get user trade orders need notify
        tradeorders = rpcaam.trade_order_list(status__in='sent, canceling')
        # get today's trade account orders
        accountorders = rpcaam.order_list(odate=datetime.date.today(), status__in='pcanceled,tcanceled,pdeal,tdeal')

        notified, failed = [], []
        # process account orders with trade orders
        for tradeorder in tradeorders:
            for accountorder in accountorders:
                try:
                    if tradeorder['ocode'] == accountorder['tcode']:
                        if accountorder['status'] in ['pcanceled', 'tdeal']:
                            if accountorder['otype'] == 'buy':
                                rpcaam.trade_order_bought(id=tradeorder['id'], dprice=accountorder['dprice'], dcount=accountorder['dcount'])
                            elif accountorder['otype'] == 'sell':
                                rpcaam.trade_order_sold(id=tradeorder['id'], dprice=accountorder['dprice'], dcount=accountorder['dcount'])
                            else:
                                pass
                        elif accountorder['status'] in ['tcanceled']:
                            rpcaam.trade_order_canceled(id=tradeorder['id'])
                        elif accountorder['status'] in ['pdeal'] and datetime.datetime.now().time() > datetime.time(15, 0): # trade closed
                            if accountorder['otype'] == 'buy':
                                rpcaam.trade_order_bought(id=tradeorder['id'], dprice=accountorder['dprice'], dcount=accountorder['dcount'])
                            elif accountorder['otype'] == 'sell':
                                rpcaam.trade_order_sold(id=tradeorder['id'], dprice=accountorder['dprice'], dcount=accountorder['dcount'])
                            else:
                                pass
                        else:
                            pass

                        notified.append(str(tradeorder))
                        break
                except Exception as e:
                    failed.append(str(tradeorder)+", error: "+str(e))

        return '\ntrade(notify): \nnotified:\n%s\nfailed:\n%s\n' % ('\n'.join(notified), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('trade(notify): %s'%str(e))


def clear(*args, **kwargs):
    """
        user trade order daily clear
        kwargs:
        {
            config:{
                rpc: {
                    aam: {
                        baseurl: <baseurl>
                        key: <key>
                        safety: <True|False>
                    }
                }
            },
            callback: <url>
        }
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

        # clear user trades
        result = rpcaam.trade_clear()

        # dict -> string arrays
        cleared, failed = [str(i) for i in result['cleared']], [str(i) for i in result['failed']]

        return '\ntrade(clear): \ncleared:\n%s\nfailed:\n%s\n' % ('\n'.join(cleared), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('trade(clear): %s'%str(e))


def expire(*args, **kwargs):
    """
        user trade order daily expire
        kwargs:
        {
            config:{
                rpc: {
                    aam: {
                        baseurl: <baseurl>
                        key: <key>
                        safety: <True|False>
                    }
                }
            },
            callback: <url>
        }
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))

        # get user trade orders need to place
        tradeorders = rpcaam.trade_order_list(status='sent')

        expired, failed = [], []
        # process user trade orders
        for tradeorder in tradeorders:
            try:
                # update trade order status from tosend->sent
                rpcaam.trade_order_expired(id=tradeorder['id'])
                expired.append(str(tradeorder))
            except Exception as e:
                failed.append(str(tradeorder)+", error: "+str(e))

        return '\ntrade(expire): \nexpired:\n%s\nfailed:\n%s\n' % ('\n'.join(expired), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('trade(expire): %s'%str(e))
