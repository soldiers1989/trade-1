from .. import protocol, handler, access, provider, template


class PayHandler(handler.Handler):
    """
        get stock list
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get arguments
        args = self.cleaned_arguments

        # get stock list
        results = provider.alipay.pay()

        #self.write(results)
        #self.redirect(results)
        self.write(template.loadpage('pay.html', form=results))

