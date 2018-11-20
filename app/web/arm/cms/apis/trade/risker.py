import decimal
from cms import auth, resp, forms, remote, enum


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

            item['status'] = enum.all['trade']['status'][item['status']]
            item['optype'] = enum.all['order']['price'][item['optype']]

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
def stoploss(request):
    """
        close the trade which reach stop loss line
    :param request:
    :return:
    """
    # get stop loss user trade
    usertrades = remote.aam.trade_risk_get('stoploss')

    # close the user trade
    for usertrade in usertrades:
        remote.aam.trade_user_sell(user=usertrade['user_id'], trade=usertrade['id'], optype='sj', oprice='0.00', ocount=usertrade['fcount'], type='close')

    data = {
        'total': len(usertrades)
    }

    # response data
    return resp.success(data=data)