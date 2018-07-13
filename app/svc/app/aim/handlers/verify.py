"""
    service verifier, including image, sms
"""
from app.util import sms, image, rand, validator
from app.aim import access, handler, error, protocol, config, models, verify, msgtpl


class CodeHandler(handler.Handler):
    @access.exptproc
    def post(self):
        """
            get verify code
        :return:
        """
        # get arguments
        t = self.get_argument('t')  # image code type, n - number, s - alpha string, ns - alpha/number string
        l = int(self.get_argument('l'))  # code length

        # check verify code length
        if not validator.range(l, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate random characters
        code = rand.vcode(t, l)
        if code is None:
            raise error.invalid_parameters

        # generate verify code id
        id = rand.uuid()

        # save to verify code storage
        verify.image.set(id, code, config.EXPIRE_VERIFY_CODE)

        # response with verify code id
        data = {'id': id}
        self.write(protocol.success(data = data))


class GeneralImageHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        i = self.get_argument('i') # verify code id
        w = int(self.get_argument('w')) # image width
        h = int(self.get_argument('h')) # image height
        f = [] # font sizes, split by ','
        for s in self.get_argument('f').split(','):
            f.append(int(s))

        # get image code from verify code storage
        code = verify.image.get(i)
        if code is None:
            raise error.invalid_parameters

        # create image
        data = image.create(code, w, h, f)

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
        sc = verify.image.get(i)

        # verify user input code
        if sc is None or c.lower() != sc.lower():
            raise error.wrong_image_verify_code

        self.write(protocol.success())


class SessionImageHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        i = self.session.id # use session id for image id
        t = self.get_argument('t') # image code type, n - number, s - alpha string, ns - alpha/number string
        l = int(self.get_argument('l')) # code length
        w = int(self.get_argument('w')) # image width
        h = int(self.get_argument('h')) # image height

        f = [] # font sizes, split by ','
        for s in self.get_argument('f').split(','):
            f.append(int(s))

        # generate random characters
        code = rand.vcode(t, l)
        if code is None:
            raise error.invalid_parameters

        # check verify code length
        if not validator.range(l, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # check image width and height
        if not validator.range(w, config.WIDTH_VERIFY_IMAGE_MIN, config.WIDTH_VERIFY_IMAGE_MAX) or not validator.range(h, config.HEIGHT_VERIFY_IMAGE_MIN, config.HEIGHT_VERIFY_IMAGE_MAX):
            raise error.invalid_parameters

        # create image
        data = image.create(code, w, h, f)

        # save verify characters
        verify.image.set(i, code, config.EXPIRE_VERIFY_CODE)

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
        i = self.session.id  # use session id for image id
        c = self.get_argument('c') # user input characters

        # get verify characters from session
        sc = verify.image.get(i)

        # verify
        if sc is None or c.lower() != sc.lower():
            raise error.wrong_image_verify_code

        self.write(protocol.success())


class GeneralSmsHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get arguments
        p = self.get_argument('p') # phone number
        c = self.get_argument('c') # user input verify code
        v = self.get_argument('v') # server verify code id
        t = self.get_argument('t') # message template
        l = int(self.get_argument('l')) # length of numbers

        # check phone number
        if not validator.phone(p):
            raise error.invalid_parameters

        # check verify code
        sc = verify.image.get(v)
        if sc is None or c.lower() != sc.lower():
            raise error.wrong_image_verify_code

        # get message template
        tpl = msgtpl.sms.get(t)
        if tpl is None:
            raise error.invalid_parameters

        # check verify code length
        if not validator.range(l, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate verify code
        code = rand.num(l)

        # save verify code
        verify.sms.set(p, code, config.EXPIRE_VERIFY_CODE)

        # send message by template
        sms.send(p, tpl.format(code))

        # response data
        data = {'expires': config.EXPIRE_VERIFY_CODE}
        self.write(protocol.success(data = data))

    @access.exptproc
    def post(self):
        """
            check sms
        :return:
        """
        # get arguments
        p = self.get_argument('p') # phone number
        c = self.get_argument('c')  # user input characters

        # verify code
        sc = verify.sms.get(p)
        if sc is None or c.lower() != sc.lower():
            raise error.wrong_sms_verify_code

        # response success
        self.write(protocol.success())


class UserSmsHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get login user phone number
        p = self.session.get('phone')
        if p is None:
            raise error.user_not_login

        # get arguments
        t = self.get_argument('t') # message template
        l = int(self.get_argument('l')) # length of numbers

        # check phone number
        if not validator.phone(p):
            raise error.invalid_parameters

        # get message template
        tpl = msgtpl.sms.get(t)
        if tpl is None:
            raise error.invalid_parameters

        # check verify code length
        if not validator.range(l, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate verify code
        code = rand.num(l)

        # save verify code
        verify.sms.set(p, code, config.EXPIRE_VERIFY_CODE)

        # send message by template
        sms.send(p, tpl.format(code))

        # response data
        data = {'expires': config.EXPIRE_VERIFY_CODE}
        self.write(protocol.success(data = data))

    @access.exptproc
    def post(self):
        """
            check sms
        :return:
        """
        # get login user phone number
        p = self.session.get('phone')
        if p is None:
            raise error.user_not_login

        # get arguments
        c = self.get_argument('c')  # user input characters

        # verify code
        sc = verify.sms.get(p)
        if sc is None or c.lower() != sc.lower():
            raise error.wrong_sms_verify_code

        # response success
        self.write(protocol.success())
