from .. import message, protocol, handler, access


class Send(handler.Handler):
    """
        send a short message
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
        :return:
        """
        # params
        params = self.cleaned_arguments

        # get arguments
        phone, business, tpl  = self.get_argument('phone'), self.get_argument('business'), self.get_argument('tpl')

        # remove params which is not for message template
        del params['phone']
        del params['business']
        del params['tpl']

        # send message
        result = message.send(phone, business, tpl, **params)

        self.write(protocol.success(data=result))
