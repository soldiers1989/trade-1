"""
    aam rpc error
"""


class AamApiError(Exception):
    """
        crond api error
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)