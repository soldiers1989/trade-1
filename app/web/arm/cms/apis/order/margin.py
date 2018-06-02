from adb import models
from cms import auth
from cms.apis import resp


@auth.need_permit
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        # get order id
        id = request.GET['id']

        # get margin records of order
        items = models.TradeMargin.objects.filter(trade__id=id)

        data = []
        for item in items:
            d = item.dict()
            data.append(d)
        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))
