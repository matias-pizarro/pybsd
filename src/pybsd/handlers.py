# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import copy
import ipaddress
import logging
import unipath

__logger__ = logging.getLogger('pybsd')


class BaseJailHandler(object):
    default_jail_root = '/usr/jails'
    jail_class_ids = {'service': 1,
                      'web': 2}

    def __init__(self, master=None, jail_root=None):
        super(BaseJailHandler, self).__init__()
        self.master = master
        j = jail_root or '/usr/jails'
        self.jail_root = unipath.Path(j)

    @classmethod
    def get_base_ip(cls, _if, jail):
        if _if.version == 4:
            ip = _if.ip.exploded.split('.')
            ip[2] = str(jail.jail_class_id)
            ip[3] = str(jail.uid)
            ip_as_string = '{}/{}'.format('.'.join(ip), str(_if.network.prefixlen))
        else:
            ip = _if.ip.exploded.split(':')
            ip[5] = str(jail.jail_class_id)
            ip[6] = str(jail.uid)
            ip_as_string = '{}/{}'.format(':'.join(ip), str(_if.network.prefixlen))
        return ipaddress.ip_interface(ip_as_string)

    @classmethod
    def extract_if(cls, master_if, jail):
        _if = copy.deepcopy(master_if)
        if _if.main_ifv4:
            _ifv4 = cls.get_base_ip(_if.main_ifv4, jail=jail)
            _if.ifsv4.clear()
            _if.ifsv4.add(_ifv4)
        if _if.main_ifv6:
            _ifv6 = cls.get_base_ip(_if.main_ifv6, jail=jail)
            _if.ifsv6.clear()
            _if.ifsv6.add(_ifv6)
        return _if

    def get_jail_path(self, jail):
        return self.jail_root.child(jail.name)

    def get_jail_ext_if(self, jail):
        return self.extract_if(self.master.j_if, jail=jail)

    def get_jail_lo_if(self, jail):
        return self.extract_if(self.master.jlo_if, jail=jail)
