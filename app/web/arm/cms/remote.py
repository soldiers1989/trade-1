"""
    remote service access by rpc
"""
from . import config, rpc

aam = rpc.aam.Aam(config.REMOTES['aam'][config.MODE]['baseurl'], config.REMOTES['aam'][config.MODE]['key'], config.REMOTES['aam'][config.MODE]['safety'])
atm = rpc.atm.Atm(config.REMOTES['atm'][config.MODE]['baseurl'], config.REMOTES['atm'][config.MODE]['key'], config.REMOTES['atm'][config.MODE]['safety'])
mds = rpc.tms.Mds(config.REMOTES['mds'][config.MODE]['baseurl'], config.REMOTES['mds'][config.MODE]['key'], config.REMOTES['mds'][config.MODE]['safety'])
crond = rpc.tms.Crond(config.REMOTES['crond'][config.MODE]['baseurl'], config.REMOTES['crond'][config.MODE]['key'], config.REMOTES['crond'][config.MODE]['safety'])