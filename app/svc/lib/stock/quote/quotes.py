"""
    quote service manager
"""
from lib.stock.quote import sina, ifeng, emoney, error


class Quotes:
    """
        quotes
    """
    def __init__(self):
        """
            init quote service
        """
        self._quotes = [
            sina.quote.SinaQuote(),
            ifeng.quote.IfengQuote(),
            emoney.quote.EmoneyQuote()
        ]

    def get(self, code):
        """
            get quote
        :param code:
        :return:
        """
        # get vendor
        vendor = self.vendor()
        while vendor is not None:
            try:
                result = vendor.get(code)
                return result
            except error.NoneServerError as e:
                # get next usable vendor
                vendor = self.vendor()

    def gets(self, codes):
        """
            get quotes
        :param codes:
        :param retry:
        :return:
        """

        # get vendor
        vendor = self.vendor()
        while vendor is not None:
            try:
                result = vendor.gets(codes)
                return result
            except error.NoneServerError as e:
                # get next usable vendor
                vendor = self.vendor()

    def status(self):
        """
            get status
        :param name:
        :return:
        """
        results = []
        for quote in self._quotes:
            results.append(quote.status())
        return results

    def vendor(self):
        """
            get first usable vendor for request
        :return:
        """
        # select a usable quote
        for q in self._quotes:
            if not q.disabled:
                return q

        # no host can be used
        return None
