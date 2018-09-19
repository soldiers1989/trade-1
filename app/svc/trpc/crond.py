"""
    quote api
"""
import requests
from tlib import token

# base url for remote crond service
_BaseUrl = "http://localhost:10001"

# token for access remote trade service
_ENABLE_KEY = True
_PRIVATE_KEY = "abc"


class CrondApiError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


def _make_token(params):
    """
        add token to params
    :param params:
    :return:
    """
    if not _ENABLE_KEY:
        return params

    return token.generate(params, _PRIVATE_KEY)


def add_task(id, name, cond, remoteurl):
    """
        add a new crond task
    :param id:
    :param name:
    :param cond:
    :param url:
    :return:
    """
    url = _BaseUrl+"/task/add"

    params = {
        'id': id,
        'name': name,
        'cond': cond,
        'url': remoteurl,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def del_task(id):
    """
        delete a timer task
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/del"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def clear_task():
    """
        clear all timer task
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/clear"

    params = {
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def disable_task(id):
    """
        disable a timer task
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/disable"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def enable_task(id):
    """
        enable a timer task
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/enable"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def execute_task(id):
    """
        enable a timer task
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/execute"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise CrondApiError(resp.get('msg'))


def get_status(id = None):
    """
        get status of all time task or specified @id
    :param id:
    :return:
    """
    url = _BaseUrl+"/task/status"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    return resp


def get_detail(id):
    """
        get task detial by task @id
    :param id:
    :return:
    """
    url = _BaseUrl + "/task/detail"

    params = {
        'id': id,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    return resp
