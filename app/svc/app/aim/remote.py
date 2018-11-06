"""
    remote service access
"""
from . import config
from tms import rpc


# remote short message service
sms = rpc.Sms(config.REMOTES['sms'][config.MODE]['baseurl'], config.REMOTES['sms'][config.MODE]['key'], config.REMOTES['sms'][config.MODE]['safety'])