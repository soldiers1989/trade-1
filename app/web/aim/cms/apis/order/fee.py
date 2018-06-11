from cms.apis import resp
from cms import auth, models


@auth.protect
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
        items = models.TradeFee.objects.filter(trade__id=id)

        data = []
        for item in items:
            d = item.dict()
            data.append(d)
        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))
