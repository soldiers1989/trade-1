"""
    quote service manager
"""
from sec.stock.quote import quote, config, sina, ifeng, emoney


class Vendor:
    def __init__(self, id, obj, disable=False):
        self._id = id
        self._obj = obj
        self._disable = disable

    def get(self, code, retry):
        return self._obj.get(code, retry)

    def gets(self, codes, retry):
        return self._obj.gets(codes, retry)

    def status(self):
        s = self._obj.status()
        s.update({'disabled': self._disable})
        return s

    def detail(self):
        return self._obj.detail()

    @property
    def id(self):
        return self._id

    @property
    def disabled(self):
        return self._disable

    def disable(self):
        self._disable = True

    def enable(self):
        self._disable = False


class Quotes:
    """
        quotes
    """
    def __init__(self, vendors={}, timeout=config.TIMEOUT, kickout=config.KICKOUT):
        """
            init quote service
        :param vendors: dict, quote source with hosts, e.g.
                {
                    'sina': ['219.142.78.242','111.161.68.235'],
                    'ifeng': ['123.103.93.161', '123.103.93.162'],
                    'emoney': ['61.129.249.13', '117.184.38.228']
                }
        :param timeout: float or tuple(float, float), connect timeout & read timeout in seconds for connection
            like: 0.1, (0.1, 0.2)
        :param kickout: int, , host failed kickout in count
        """
        # all quote data sources
        self._vendors = []

        # add sina
        self._vendors.append(Vendor(sina.ID, sina.quote.SinaQuote(vendors.get(sina.ID, []), timeout, kickout)))

        # add ifeng
        self._vendors.append(Vendor(ifeng.ID, ifeng.quote.IfengQuote(vendors.get(ifeng.ID, []), timeout, kickout)))

        # add east money
        self._vendors.append(Vendor(emoney.ID, emoney.quote.EmoneyQuote(vendors.get(emoney.ID, []), timeout, kickout)))

        # roll index for vendors
        self._vindex = 0
        # vendor count
        self._vcount = len(self._vendors)

    def get(self, code, retry=config.RETRY):
        """
            get quote
        :param code:
        :param retry:
        :return:
        """
        vendor = self._next_vendor()
        if vendor is not None:
            return vendor.get(code, retry)
        return None

    def gets(self, codes, retry=config.RETRY):
        """
            get quotes
        :param codes:
        :param retry:
        :return:
        """
        vendor = self._next_vendor()
        if vendor is not None:
            return vendor.gets(codes, retry)
        return None

    def status(self, id=None):
        """
            get vendor status
        :param name:
        :return:
        """
        if id is None:
            results = []
            for vendor in self._vendors:
                results.append(vendor.status())
            return results

        for vendor in self._vendors:
            if vendor.id == id:
                return vendor.detail()

        return None

    def enable(self, id):
        """
            enable a vendor by name
        :param id:
        :return:
        """
        for vendor in self._vendors:
            if vendor.id == id:
                vendor.enable()
                break

    def disable(self, id):
        """
            disable a vendor
        :param id:
        :return:
        """
        for vendor in self._vendors:
            if vendor.id == id:
                vendor.disable()
                break

    def _next_vendor(self):
        """
            get next vendor for request
        :return:
        """
        # select a enabled vendor
        for i in range(0, self._vcount):
            vendor = self._vendors[self._vindex % self._vcount]
            self._vindex += 1
            if not vendor.disabled:
                return vendor

        # no host can be used
        return None