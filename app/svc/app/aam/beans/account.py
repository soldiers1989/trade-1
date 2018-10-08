"""
    account beans
"""
from .. import forms, daos, mysql


def select(form: forms.account.Select):
    """
        select a account for buying
    :param form: obj,
    :return:
        account object
    """
    # connect database
    db = mysql.get()

    # init dao object
    dao = daos.account.AccountDao(db)

    # select relate usable accounts
    accounts = dao.list(type=form.type, disable=False)
    if len(accounts) == 0:
        return None

    # sort by left money desc
    accounts.sort(key=lambda x: x['lmoney'], reverse=True)

    # select max left money account
    return accounts[0]
