"""
    user handlers
"""
from app.aim import access, handler, protocol


class LoginHandler(handler.Handler):
    @access.protect
    def get(self):
        """
            echo
        :return:
        """
        try:
            self.write(protocol.success(data=[]))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))

