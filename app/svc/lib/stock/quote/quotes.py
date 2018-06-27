"""
    quote service manager
"""
from lib.stock.quote import config, sina, ifeng, emoney, error


class Vendor:
    def __init__(self, id, obj, disabled=False):
        self._id = id
        self._obj = obj
        self._disabled = disabled

    def get(self, code, retry):
        return self._obj.get(code, retry)

    def gets(self, codes, retry):
        return self._obj.gets(codes, retry)

    def status(self):
        s = self._obj.status()
        s.update({'disabled': self._disabled})
        return s

    def detail(self):
        return self._obj.detail()

    @property
    def id(self):
        return self._id

    @property
    def disabled(self):
        return self._disabled

    def disable(self):
        self._disabled = True

    def enable(self):
        self._disabled = False


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


    def get(self, code, retry=config.RETRY):
        """
            get quote
        :param code:
        :param retry:
        :return:
        """
        # quote result
        result = None

        # get vendor
        vendor = self.vendor()
        while vendor is not None:
            try:
                result = vendor.get(code, retry)
                return result
            except error.HostLackError as e:
                # disable current vendor
                vendor.disable()
                # get next usable vendor
                vendor = self.vendor()

    def gets(self, codes, retry=config.RETRY):
        """
            get quotes
        :param codes:
        :param retry:
        :return:
        """
        # quote result
        results = None

        # get vendor
        vendor = self.vendor()
        while vendor is not None:
            try:
                result = vendor.gets(codes, retry)
                return result
            except error.HostLackError as e:
                # disable current vendor
                vendor.disable()
                # get next usable vendor
                vendor = self.vendor()

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

    def enable(self, id=None):
        """
            enable a vendor by name
        :param id:
        :return:
        """
        if id is not None:
            for vendor in self._vendors:
                if vendor.id == id:
                    vendor.enable()
                    break
        else:
            for vendor in self._vendors:
                vendor.enable()

    def disable(self, id=None):
        """
            disable a vendor
        :param id:
        :return:
        """
        if id is not None:
            for vendor in self._vendors:
                if vendor.id == id:
                    vendor.disable()
                    break
        else:
            for vendor in self._vendors:
                vendor.disable()

    def vendor(self):
        """
            get first usable vendor for request
        :return:
        """
        # select a enabled vendor
        for v in self._vendors:
            if not v.disabled:
                return v

        # no host can be used
        return None
