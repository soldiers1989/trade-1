from app.atm import config
from app.util import mysql

# mysql databases
_atm = config.DATABASES['atm'][config.MODE]


# mysql object
def get():
    """
        get a mysql object
    :return:
    """
    return mysql.DBMysql(_atm)


