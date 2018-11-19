"""
    remote service access
"""
from . import config, rpc


# remote short message service
sms = rpc.tms.Sms(config.REMOTES['sms'][config.MODE]['baseurl'], config.REMOTES['sms'][config.MODE]['key'], config.REMOTES['sms'][config.MODE]['safety'])