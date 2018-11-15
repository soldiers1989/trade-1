"""
    process account orders
"""
import datetime
from .. import remote


def take(*args, **kwargs):
    """
        table not-send account orders, make them to to-send
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

        # take orders not send
        result = rpcaam.order_take()

        # get response
        taked, failed = [str(i) for i in result['taked']], [str(i) for i in result['failed']]

        return '\norder(take): \ntaked:\n%s\nfailed:\n%s\n' % ('\n'.join(taked), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('order(take): %s'%str(e))


def place(*args, **kwargs):
    """
        place not-send order to trade account which connect the securities counter
        kwargs:
        {
            "config":{
                "rpc": {
                    "aam": {
                        "baseurl": "http://localhost:9001",
                        "key": "abc",
                        "safety": false
                    },
                    "trade": {
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
        rpctrade = remote.tms.Trade(config['rpc']['trade']['baseurl'], config['rpc']['trade'].get('key'), config['rpc']['trade'].get('safety', False))

        # get account orders need to place
        accountorders = rpcaam.order_list(status__in='tosend, tocancel', odate=datetime.date.today())

        placed, failed = [], []
        # process user trade orders
        for accountorder in accountorders:
            try:
                if accountorder['status'] == 'tosend':
                    # update account order status from tosend->sending
                    rpcaam.order_sending(id=accountorder['id'])
                    # send order to securities counter
                    resp = rpctrade.place(account=accountorder['account'], otype=accountorder['otype'], ptype=accountorder['optype'],
                                   zqdm=accountorder['scode'], price=accountorder['oprice'], count=accountorder['ocount'])
                    # update account order status from sending->sent
                    rpcaam.order_sent(id=accountorder['id'], ocode=resp[0]['wtbh'])
                elif accountorder['status'] == 'tocancel':
                    # cancel order in securities counter
                    rpctrade.cancel(account=accountorder['account'], zqdm=accountorder['scode'], orderno=accountorder['ocode'])
                    # update account order status from tocancel->canceling
                    rpcaam.order_canceling(id=accountorder['id'])
                else:
                    pass

                placed.append(str(accountorder))
            except Exception as e:
                failed.append(str(accountorder)+", error: "+str(e))

        return '\norder(place): \nplaced:\n%s\nfailed:\n%s\n' % ('\n'.join(placed), '\n'.join(failed))
    except Exception as e:
        raise RuntimeError('order(place): %s'%str(e))


def notify(*args, **kwargs):
    """
        sync the order status from securities counter
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # get config
        config, callback = kwargs.get('config'), kwargs.get('callback')

        # init remote rpc
        rpcaam = remote.aam.Aam(config['rpc']['aam']['baseurl'], config['rpc']['aam'].get('key'), config['rpc']['aam'].get('safety', False))
        rpctrade = remote.tms.Trade(config['rpc']['trade']['baseurl'], config['rpc']['trade'].get('key'), config['rpc']['trade'].get('safety', False))


        # get today's pending account order's accounts
        accounts = rpcaam.order_accounts(status__in='sent,tocancel,canceling,pdeal', odate=datetime.date.today())

        notified, failed, errors = [], [], []
        # get each account today's orders
        for account in accounts:
            try:
                notifyorders = []
                # get today's order from trade service
                orders = rpctrade.query(account=account, type='drwt')
                for order in orders:
                    notifyorders.append({
                        'account': account,
                        'ocode': order['wtbh'],
                        'dprice': order['cjjg'],
                        'dcount': order['cjsl'],
                        'status': order['ztsm'],
                        'operator': 'sys'
                    })

                # notify order to aam service
                results = rpcaam.order_notify(json=notifyorders)

                # notify results
                notified.extend([str(i) for i in results['notified']])
                failed.extend([str(i) for i in results['failed']])
            except Exception as e:
                errors.append('notify account: '+str(e))

        return '\norder(notify): \nnotified:\n%s\nfailed:\n%s\nerrors:\n%s\n' % ('\n'.join(notified), '\n'.join(failed), '\n'.join(errors))
    except Exception as e:
        raise RuntimeError('order(notify): %s'%str(e))

