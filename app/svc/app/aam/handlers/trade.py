"""
    service admin
"""
from app.aam import access, handler, protocol, redis, error, log


class AddHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        # get arguments
        userid, couponid, leverid, stockid, ptype, price, count = self.get_argument('uid'), self.get_argument('cid'), self.get_argument('lid'), \
                                                                  self.get_argument('stock'), self.get_argument('ptype'), self.get_argument('price'), \
                                                                  self.get_argument('count')

        # check arguments


        pass
