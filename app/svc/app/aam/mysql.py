from tlib import mysql
from . import config

# mysql databases
_aam = config.DATABASES['aam'][config.MODE]


# mysql object
def get():
    """
        get a mysql object
    :return:
    """
    return mysql.DBMysql(_aam)
