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
