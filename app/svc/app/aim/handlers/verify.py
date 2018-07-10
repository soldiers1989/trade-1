"""
    service verifier, including image, sms
"""
from app.util import sms, image, rand
from app.aim import access, handler, error, protocol, config, cache, vcode


class ImageCodeHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verify code id
        :return:
        """
        # get arguments
        u = self.get_argument('u') # verify code usage

        # get verify code object by usage
        o = vcode.create(u)

        if o is None:
            self.write(error.wrong_usage_verify_code.data)
            return

        data = {'v': o.id}
        self.write(protocol.success(data = data))


class SmsCodeHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verify code id
        :return:
        """
        # get arguments
        u = self.get_argument('u') # verify code usage

        # get verify code object by usage
        o = vcode.create(u)

        if o is None:
            self.write(error.wrong_usage_verify_code.data)
            return

        data = {'v': o.id}
        self.write(protocol.success(data = data))


class ImageHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        i = self.get_argument('i') # identifier for usage
        t = self.get_argument('t') # image code type, n - number, s - alpha string, ns - alpha/number string
        l = int(self.get_argument('l')) # code length
        w = int(self.get_argument('w')) # image width
        h = int(self.get_argument('h')) # image height

        f = [] # font sizes, split by ','
        for s in self.get_argument('f').split(','):
            f.append(int(s))

        # generate random characters
        if t == 'n':
            chars = rand.num(l)
        elif t == 's':
            chars = rand.alpha(l)
        elif t == 'ns':
            chars = rand.alnum(l)
        else:
            chars = rand.num(l)

        # create image
        data = image.create(chars, w, h, f)

        # save verify characters
        cache.img.set(self.session.id, i, chars, config.EXPIRE_VERIFIER_IMAGE)

        # response image data
        self.set_header('Content-Type', 'image/png')
        self.write(data)

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
        sc = cache.img.get(self.session.id, i)

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
        msg = rand.num(l)
        cache.sms.set(p, i, msg, config.EXPIRE_VERIFIER_SMS)

        # send message
        sms.send(p, msg)

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
        sc = cache.sms.get(p, i)
        if sc is not None and c.lower() == sc.lower():
            self.write(protocol.success())
        else:
            self.write(error.wrong_sms_verify_code.data)


class PhoneSmsHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get arguments
        p = self.get_argument('p') # phone number
        u = self.get_argument('u') # verify code usage
        c = self.get_argument('c') # user input verify code for send message

        # create verify vode
        vcode = rand.num(l)
        cache.sms.set(p, i, msg, config.EXPIRE_VERIFIER_SMS)

        # send message
        sms.send(p, msg)

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
        sc = cache.sms.get(p, i)
        if sc is not None and c.lower() == sc.lower():
            self.write(protocol.success())
        else:
            self.write(error.wrong_sms_verify_code.data)


class UserSmsHandler(handler.Handler):
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
        msg = rand.num(l)
        cache.sms.set(p, i, msg, config.EXPIRE_VERIFIER_SMS)

        # send message
        sms.send(p, msg)

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
        sc = cache.sms.get(p, i)
        if sc is not None and c.lower() == sc.lower():
            self.write(protocol.success())
        else:
            self.write(error.wrong_sms_verify_code.data)