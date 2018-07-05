"""
    service verifier, including image, sms
"""
from app.util import verifier
from app.aim import log, access, handler, error, protocol, session


class ImageHandler(handler.Handler):
    def get(self):
        """
            echo
        :return:
        """
        t = self.get_argument('t', 'n')
        n = int(self.get_argument('n', verifier._LENGTH))
        w = int(self.get_argument('w', verifier._WIDTH))
        h = int(self.get_argument('h', verifier._HEIGHT))

        imgdata = None
        if t == 'n':
            imgdata = verifier.randnimg(n, w, h)
        elif t == 's':
            imgdata = verifier.randsimg(n, w, h)
        elif t == 'ns':
            imgdata = verifier.randnsimg(n, w, h)
        else:
            imgdata = verifier.randnimg(n, w, h)

        self.set_header('Content-Type', 'image/png')
        self.write(imgdata)


class SmsHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        self.write(protocol.success(msg='success', data='echo'))
