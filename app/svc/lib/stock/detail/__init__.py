from lib.stock.detail import sina, cninfo


class _Sina:
    @staticmethod
    def list():
        return sina.list.fetch()


sina = _Sina


class _CNInfo:
    @staticmethod
    def list():
        return cninfo.list.fetch()


cninfo = _CNInfo
