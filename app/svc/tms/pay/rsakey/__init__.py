"""
    rsa keys
"""
import os


def load(relative_path):
    """
        load
    :param relative_path:
    :return:
    """
    filepath = '%s/%s' % (os.path.dirname(__file__), relative_path)
    with open(filepath) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        return ''.join(lines)