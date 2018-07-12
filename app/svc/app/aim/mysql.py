from app.aim import config
from app.util import mysql

# mysql databases
_aim = config.DATABASES['aim'][config.MODE]

# mysql object
def get():
    """
        get a mysql object
    :return:
    """
    return mysql.DBMysql(_aim)


