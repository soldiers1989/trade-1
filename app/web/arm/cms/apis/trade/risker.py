import time, decimal
from adb import models
from cms import auth, resp, forms, remote, enum, error, config


@auth.catch_exception
@auth.need_login
def list(request):
    """
        list specified type trade list
    :param request:
    :return:
    """
    form = forms.trade.risker.Get(request.GET)
    if form.is_valid():
        # get parameter
        type = form.cleaned_data.get('type')

        # request rpc
        result = remote.aam.trade_risk_get(type)

        # compute total capital/market-value/margin/ofee/dfee
        capital, marketv, margin, ofee, dfee = decimal.Decimal('0.00'), decimal.Decimal('0.00'), decimal.Decimal('0.00'), decimal.Decimal('0.00'), decimal.Decimal('0.00')
        for item in result:
            capital += decimal.Decimal(item['capital'])
            marketv += decimal.Decimal(item['marketv'])
            margin += decimal.Decimal(item['margin'])
            ofee +=  decimal.Decimal(item['ofee'])
            dfee +=  decimal.Decimal(item['dfee'])

            item['_status'] = enum.all['trade']['status'][item['status']]
            item['_optype'] = enum.all['order']['price'][item['optype']]

        # convert data
        data = {
            'total': len(result),
            'rows': result,
            'brief': {
                'capital': capital,
                'marketv': marketv,
                'margin': margin,
                'ofee': ofee,
                'dfee': dfee
            }
        }

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def check(request):
    """
        check risk
    :param request:
    :return:
    """
    # service config
    jsondata = {
        "config":{
            "rpc":{
                "aam": config.REMOTES["aam"][config.MODE],
                "mds": config.REMOTES["mds"][config.MODE]
            }
        },
        "callback":""
    }

    # risk check
    remote.atm.risk_check(jsondata)

    # response data
    data = {
        "time": int(time.time())
    }

    return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def sell(request):
    """
        close the trade which reach stop loss line
    :param request:
    :return:
    """
    form = forms.trade.risker.Sell(request.POST)
    if form.is_valid():
        # get trade id
        id = form.cleaned_data.get('id')
        if id is None or id=='':
            # get all stop loss user trade
            closetrades = remote.aam.trade_risk_get('stoploss')

            # close the user trade
            closed, failed = [], []
            for closetrade in closetrades:
                try:
                    # get user trade from database
                    usertrade = models.UserTrade.objects.filter(id=closetrade['id']).first()
                    if usertrade is None:
                        raise error.trade_not_exist
                    if usertrade.status != 'hold':
                        raise error.trade_operation_denied
                    if usertrade.fcount == 0:
                        raise error.trade_no_free_position
                    if usertrade.fcount != usertrade.hcount:
                        raise error.trade_position_confused

                    # send sell order
                    remote.aam.trade_user_sell(user=usertrade.user_id, trade=usertrade.id, optype='sj', oprice='0.00', ocount=usertrade.fcount, type='close')

                    # record the orde
                    closed.append(str(usertrade.id))
                except Exception as e:
                    failed.append('%s,%s' % (id, e))

            # response data
            data = {
                'closed': ','.join(closed),
                'failed': '\n'.join(failed)
            }
        else:
            # get user trade from database
            usertrade = models.UserTrade.objects.filter(id=id).first()
            if usertrade is None:
                raise error.trade_not_exist
            if usertrade.status != 'hold':
                raise error.trade_operation_denied
            if usertrade.fcount == 0:
                raise error.trade_no_free_position
            if usertrade.fcount != usertrade.hcount:
                raise error.trade_position_confused

            # send sell order
            remote.aam.trade_user_sell(user=usertrade.user_id, trade=usertrade.id, optype='sj', oprice='0.00', ocount=usertrade.fcount, type='close')

            # response data
            data = {
                'closed': str(usertrade.id)
            }

        return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def cancel(request):
    """
        cancel close operation
    :param request:
    :return:
    """
    form = forms.trade.risker.Cancel(request.POST)
    if form.is_valid():
        # get trade id
        id = form.cleaned_data.get('id')

        # get user trade from database
        usertrade = models.UserTrade.objects.filter(id=id).first()
        if usertrade is None:
            raise error.trade_not_exist
        if usertrade.status not in ['toclose', 'closing'] :
            raise error.trade_operation_denied

        # send sell order
        remote.aam.trade_user_cancel(user=usertrade.user_id, trade=usertrade.id)

        # response data
        data = {
            'canceled': str(usertrade.id)
        }

        return resp.success(data=data)
