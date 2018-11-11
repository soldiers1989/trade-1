"""
    remote service access by rpc
"""
from . import config, rpc

aam = rpc.Aam(config.REMOTES['aam'][config.MODE]['baseurl'], config.REMOTES['aam'][config.MODE]['key'], config.REMOTES['aam'][config.MODE]['safety'])