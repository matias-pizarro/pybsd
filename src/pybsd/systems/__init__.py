# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import logging
import re
from .network import Interface


__logger__ = logging.getLogger('pybsd')
IF_PROPERTY = re.compile(r'^_\w*_if$')


class SystemError(Exception):
    def __init__(self, *args, **kwargs):
        super(SystemError, self).__init__(*args, **kwargs)
        if six.PY3:
            self.message = args[0]


class BaseSystem(object):
    """Describes a base OS instance, as a computer, a virtualized system or a jail"""

    def __init__(self, name, hostname=None):
        super(BaseSystem, self).__init__()
        self.name = name
        self.hostname = (hostname or name)


class System(BaseSystem):
    """Describes a full OS instance"""

    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None):
        super(System, self).__init__(name=name, hostname=hostname)
        self.ext_if = ext_if
        self.int_if = int_if
        self.lo_if = lo_if

    @property
    def ext_if(self):
        return self._ext_if

    @ext_if.setter
    def ext_if(self, _if):
        if_name, if_ips = _if
        _ext_if = Interface(name=if_name, ips=if_ips)
        intersec = _ext_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._ext_if = _ext_if

    @property
    def int_if(self):
        return self._int_if or self.ext_if

    @int_if.setter
    def int_if(self, _if):
        if _if:
            if_name, if_ips = _if
            _int_if = Interface(name=if_name, ips=if_ips)
            intersec = _int_if.ips.intersection(self.ips)
            if len(intersec):
                raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _int_if != self.ext_if:
                self._int_if = _int_if
        else:
            self._int_if = None

    @property
    def lo_if(self):
        return self._lo_if

    @lo_if.setter
    def lo_if(self, _if):
        if _if:
            if_name, if_ips = _if
        else:
            if_name = 'lo0'
            if_ips = ['127.0.0.1/8', '::1/128']
        _lo_if = Interface(name=if_name, ips=if_ips)
        intersec = _lo_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._lo_if = _lo_if

    @property
    def ips(self):
        ips = set()
        for prop, interface in six.iteritems(self.__dict__):
            if IF_PROPERTY.match(prop) and interface:
                ips.update([x.ip.compressed for x in interface.ifsv4])
                ips.update([x.ip.compressed for x in interface.ifsv6])
        return ips
