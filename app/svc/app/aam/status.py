import json, time


def append(operator, action, before, after, detail, logstr=None):
    """

    :param operator:
    :param action:
    :param before:
    :param after:
    :param detail:
    :return:
    """
    logs = [] if logstr is None else json.loads(logstr)
    logs.append({
        'user': operator,
        'action': action,
        'before': before,
        'after': after,
        'detail': detail,
        'time': int(time.time())
    })

    return json.dumps(logs)


def trade_detail(**kwargs):
    """
        user trade log detail, format:
        account,optype,oprice,ocount,hprice,hcount,fcount,bprice,bcount,sprice,scount
    :param kwargs:
    :return:
    """
    return '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (kwargs.get('account'), kwargs.get('optype'), kwargs.get('oprice'), kwargs.get('ocount'),
                                                               kwargs.get('hprice'), kwargs.get('hcount'), kwargs.get('fcount'), kwargs.get('bprice'),
                                                               kwargs.get('bcount'), kwargs.get('sprice'),kwargs.get('scount'))


def order_detail(**kwargs):
    """
        account/trade order log detail, format:
        otype, optype, oprice, ocount, dprice, dcount
    :param kwargs:
    :return:
    """
    return '%s, %s, %s, %s, %s, %s' % (kwargs.get('otype'), kwargs.get('optype'), kwargs.get('oprice'),
                                       kwargs.get('ocount'), kwargs.get('dprice', '0.0'), kwargs.get('dcount', 0))

