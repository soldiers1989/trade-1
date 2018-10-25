"""
    web socket protocol
"""
import websocket


class Session:
    """
        a web socket session
    """
    def __init__(self, baseurl, **kwargs):
        """
            int a web socket session
        :param baseurl: str, web socket base url address like [wss|ws]://host:port
        :param kwargs: dict, extensible arguments
        """
        self._baseurl = baseurl


class Client:
    """
        web socket client with many sessions
    """
    pass