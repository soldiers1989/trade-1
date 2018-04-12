import os, logging

default_log_level = logging.DEBUG
default_log_format = "[%(asctime)s][%(name)s][%(levelname)s]%(messsage)s[%(filename)s, %(lineno)d]"
default_log_file_dir = "./log"


def create_logger(name):
    """
        create logger by log name and file path
    :param name: string, log name
    :return:
        Logger object
    """
    # make log directory
    if not os.path.exists(default_log_file_dir):
        os.makedirs(default_log_file_dir)

    # create new logger
    logger = logging.getLogger(name);

    # create console handler
    console = logging.StreamHandler()

    # create file handler
    file = os.path.join(default_log_file_dir, name)
    handler = logging.FileHandler(file)

    # set logger level
    console.setLevel(default_log_level)
    handler.setLevel(default_log_level)

    # create formater
    formarter = logging.Formatter(default_log_format)

    # set logger formarter
    console.setFormatter(formarter)
    handler.setFormatter(formarter)

    # set handler
    logger.addHandler(console)
    logger.addHandler(handler)

    return logger

trade = create_logger("trade")

