"""
    protocol for trade service
"""
import json


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

    return json.dumps(ret)


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

    return json.dumps(ret)


def upgrade(resp, alias):
    """
        upgrade response dat
    :param resp:
    :param ialias:
    :return:
    """
    # response
    status, msg, data = resp['status'], resp['msg'], resp['data']

    ndata = data
    # translate data with alias
    if data is not None and isinstance(data, list) and len(data)>0:
        columns = {}
        for i in range(0, len(data[0])):
            name = alias.get(data[0][i])
            if name is not None:
                columns[name] = i

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
        'data': ndata
    }

    return resp
