from sec.stock.trade.tdx.protocol import alias, field, query, status


def success(msg = 'success', data = None):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': 0,
        'msg': msg,
        'data': data
    }

    return ret


def failed(msg = 'failed', data = None):
    """
        error return format
    :param msg:
    :return:
    """
    # make formatted return
    ret = {
        'status': -1,
        'msg': msg,
        'data': data
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
    columns = {}
    for i in range(0, len(data[0])):
        iname = ialias.get(data[0][i])
        if iname is not None:
            columns[iname] = i

    ndata = []
    for row in data[1:]:
        nrow = {}
        for name, index in columns.items():
            nrow[name] = row[index]
        ndata.append(nrow)

    # upgrade
    resp = {
        'status': status,
        'msg': msg,
        'data': {
            'new': ndata,
            'old': data
        }
    }

    return resp
