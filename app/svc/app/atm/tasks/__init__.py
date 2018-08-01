"""
    all tasks
"""
from app.atm import timer
from app.atm.tasks import stock


def setup():
    """
        setup all tasks
    :return:
    """
    timer.default.setup()