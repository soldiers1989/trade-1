"""
    stock api
"""
from . import config, token, error
import requests


def list():
    """
        list all stocks
    :return:
    """
    url = config.BaseUrl+"/stock/list"

    params = {
    }
    params = token.make(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise error.AamApiError(resp.get('msg'))

    return resp.get('data')


def get(id):
    """
        get stock by @id
    :param id:
    :return:
    """
    url = config.BaseUrl+"/stock/get"

    params = {
        'id': id
    }
    params = token.make(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise error.AamApiError(resp.get('msg'))

    return resp.get('data')


def add(stocks):
    """
        add new stocks
    :param stocks: list, stock list
    :return:
    """
    url = config.BaseUrl+"/stock/add"

    params = {
    }
    params = token.make(params)

    resp = requests.post(url, params=params, json=stocks).json()

    if resp.get('status') != 0:
        raise error.AamApiError(resp.get('msg'))

    return resp.get('data')
