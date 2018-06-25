from sec.stock.trade.tdx.protocol import alias, field, query, status


def error(msg):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': -1,
        'msg': msg,
        'data': {}
    }

    return ret


def upgrade(resp, ialias):
    """
        upgrade response dat
    :param resp:
    :param ialias:
    :return:
    """
    # response
    status, msg, data = resp['status'], resp['msg'], resp['data']

    # translate data with alias
    colnames, colnums = [], []
    for i in range(0, len(data[0])):
        iname = ialias.get(data[0][i])
        if iname is not None:
            colnames.append(iname)
            colnums.append(i)

    ndata = [colnames]
    for row in data[1:]:
        nrow = []
        for num in colnums:
            nrow.append(row[num])
        ndata.append(nrow)

    # upgrade
    resp = {
        'status': status,
        'msg': msg,
        'data': ndata
    }

    return resp
