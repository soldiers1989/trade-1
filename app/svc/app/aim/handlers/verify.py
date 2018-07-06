"""
    service verifier, including image, sms
"""
from app.util import verifier
from app.aim import verify, access, handler, error, protocol, config


class ImageHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        i = self.get_argument('i') # identifier for usage
        t = self.get_argument('t', 'n') # image code type, n - number, s - alpha string, ns - alpha/number string
        l = int(self.get_argument('l', verifier._DEFAULT_LENGTH)) # code length
        w = int(self.get_argument('w', verifier._DEFAULT_WIDTH)) # image width
        h = int(self.get_argument('h', verifier._DEFAULT_HEIGHT)) # image height

        # generate verify chars and image data
        chars, imgdata = None, None
        if t == 'n':
            chars, imgdata = verifier.image.num(l, w, h)
        elif t == 's':
            chars, imgdata = verifier.image.alpha(l, w, h)
        elif t == 'ns':
            chars, imgdata = verifier.image.alnum(l, w, h)
        else:
            chars, imgdata = verifier.image.num(l, w, h)

        # save verify chars
        verify.img.set(self.session.id, i, chars, config.EXPIRE_VERIFIER_IMAGE)

        # response image data
        self.set_header('Content-Type', 'image/png')
        self.write(imgdata)

    @access.exptproc
    def post(self):
        """
            check verifier image
        :return:
        """
        # get arguments
        i = self.get_argument('i') # identifier for using
        c = self.get_argument('c') # user input characters

        # get verify characters from session
        sc = verify.img.get(self.session.id, i)

        # verify
        if sc is not None and c.lower() == sc.lower():
            self.write(protocol.success())
        else:
            self.write(error.wrong_image_verify_code.data)


class SmsHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get arguments
        p = self.get_argument('p') # phone number
        i = self.get_argument('i') # identifier for usage
        l = int(self.get_argument('l', 6)) # length of numbers

        # create & save message
        msg = verifier.rand.num(l)
        verify.sms.set(p, i, msg, config.EXPIRE_VERIFIER_SMS)

        # send message
        verifier.sms.send(p, msg)

        # response
        self.write(protocol.success())

    @access.exptproc
    def post(self):
        """
            check sms
        :return:
        """
        # get arguments
        p = self.get_argument('p') # phone number
        i = self.get_argument('i') # identifier for usage
        c = self.get_argument('c')  # user input characters

        # verify code
        sc = verify.sms.get(p, i)
        if sc is not None and c.lower() == sc.lower():
            self.write(protocol.success())
        else:
            self.write(error.wrong_sms_verify_code.data)