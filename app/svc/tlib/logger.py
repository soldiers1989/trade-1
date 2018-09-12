import os, logging


_default_log_level = logging.NOTSET
_default_log_format = "[%(asctime)s][%(name)s][%(levelname)s]%(messsage)s[%(filename)s, %(lineno)d]"
_default_log_file_dir = "./log"


def create(name, logdir=_default_log_file_dir, format=_default_log_format, level=_default_log_level):
    """
        create logger by log name and file path
    :param name: string, log name
    :return:
        Logger object
    """
    # make log directory
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    # create new logger
    logger = logging.getLogger(name);

    # create console handler
    console = logging.StreamHandler()

    # create file handler
    file = os.path.join(logdir, name)
    handler = logging.FileHandler(file)

    # set logger level
    console.setLevel(level)
    handler.setLevel(level)

    # create formater
    #formarter = logging.Formatter(format)

    # set logger formarter
    #console.setFormatter(formarter)
    #handler.setFormatter(formarter)

    # set handler
    #logger.addHandler(console)
    logger.addHandler(handler)

    return logger
