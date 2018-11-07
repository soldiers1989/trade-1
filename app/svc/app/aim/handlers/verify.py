"""
    service verifier, including image, sms
"""
from tlib import rand, image, validator
from .. import access, handler, error, protocol, config, verify, msgtpl, forms, remote


class VerifyIDGetHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verify code
        :return:
        """
        # get arguments
        form = forms.verify.VerifyIDGet(**self.arguments)

        # check verify code length
        if not validator.range(form.length, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate random characters
        code = rand.vcode(form.type, form.length)
        if code is None:
            raise error.invalid_parameters

        # generate verify code id
        id = rand.uuid()

        # save to verify code storage
        verify.image.set(id, code, config.EXPIRE_VERIFY_CODE)

        # response with verify code id
        data = {
            'id': id,
            'expires': config.EXPIRE_VERIFY_CODE
        }

        self.write(protocol.success(data = data))


class VerifyImageGeneralHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        form = forms.verify.VerifyImageGeneralGet(**self.arguments)

        fonts = [] # font sizes, split by ','
        for s in form.fonts.split(','):
            fonts.append(int(s))

        # check image width and height
        if not validator.range(form.width, config.WIDTH_VERIFY_IMAGE_MIN, config.WIDTH_VERIFY_IMAGE_MAX)\
                or not validator.range(form.height, config.HEIGHT_VERIFY_IMAGE_MIN, config.HEIGHT_VERIFY_IMAGE_MAX):
            raise error.invalid_parameters

        # get image code from verify code storage
        code = verify.image.get(form.id)
        if code is None:
            raise error.invalid_parameters

        # create image
        data = image.create(code, form.width, form.height, fonts)

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
        form = forms.verify.VerifyImageGeneralPost(**self.arguments)

        # get verify characters from session
        sc = verify.image.get(form.id)

        # verify user input code
        if sc is None or form.code.lower() != sc.lower():
            raise error.wrong_image_verify_code

        self.write(protocol.success())


class VerifyImageSessionHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            get verifier image
        :return:
        """
        # get arguments
        form = forms.verify.VerifyImageSessionGet(**self.arguments)

        fonts = [] # font sizes, split by ','
        for s in form.fonts.split(','):
            fonts.append(int(s))

        id = self.session.id # use session id for image id

        # check verify code length
        if not validator.range(form.length, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # check image width and height
        if not validator.range(form.width, config.WIDTH_VERIFY_IMAGE_MIN, config.WIDTH_VERIFY_IMAGE_MAX) \
                or not validator.range(form.height, config.HEIGHT_VERIFY_IMAGE_MIN, config.HEIGHT_VERIFY_IMAGE_MAX):
            raise error.invalid_parameters

        # generate random characters
        code = rand.vcode(form.type, form.length)
        if code is None:
            raise error.invalid_parameters

        # create image
        data = image.create(code, form.width, form.height, fonts)

        # save verify characters
        verify.image.set(id, code, config.EXPIRE_VERIFY_CODE)

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
        form = forms.verify.VerifyImageSessionPost(**self.arguments)

        id = self.session.id  # use session id for image id

        # get verify characters from session
        sc = verify.image.get(id)

        # verify
        if sc is None or form.code.lower() != sc.lower():
            raise error.wrong_image_verify_code

        self.write(protocol.success())


class VerifySmsHandler(handler.Handler):
    @access.exptproc
    def get(self):
        """
            send sms
        :return:
        """
        # get arguments
        form = forms.verify.VerifySmsGet(**self.arguments)

        # check phone number
        if not validator.phone(form.phone):
            raise error.invalid_parameters

        # get message template
        tpl = msgtpl.sms.get(form.type)
        if tpl is None:
            raise error.invalid_parameters

        # check verify code length
        if not validator.range(form.length, config.LENGTH_VERIFY_CODE_MIN, config.LENGTH_VERIFY_CODE_MAX):
            raise error.invalid_parameters

        # generate verify code
        code = rand.num(form.length)

        # save verify code
        verify.sms.set(form.phone, code, config.EXPIRE_VERIFY_CODE)

        # send message by template
        remote.sms.send(form.phone, tpl.format(code))

        # response data
        data = {
            'code': code,
            'expires': config.EXPIRE_VERIFY_CODE
        }

        self.write(protocol.success(data = data))

    @access.exptproc
    def post(self):
        """
            check sms
        :return:
        """
        # get arguments
        form = forms.verify.VerifySmsPost(**self.arguments)

        # verify code
        sc = verify.sms.get(form.phone)
        if sc is None or form.code.lower() != sc.lower():
            raise error.wrong_sms_verify_code

        # response success
        self.write(protocol.success())


