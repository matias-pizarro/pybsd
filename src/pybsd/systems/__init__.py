# -*- coding: utf-8 -*-
"""The :py:mod:`~pybsd.systems` module provides classes which are used to represent a working Operating System
instances. This allows interaction with both real and modelized instances.

Examples
---------
from pybsd.systems import System
box01 = System(name='box01',
                     hostname='box01.foo.bar',
                     ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
                     int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']))
box01.ips
set(['192.168.0.0', '::1', '1c02:4f8:f0:14e6::', '148.241.178.106', '127.0.0.1', '1c02:4f8:f0:14e6::1'])


Classes
-------
"""
from __future__ import unicode_literals, print_function, absolute_import
import six
import logging
import re
from .executors import Executor
from .network import Interface

__logger__ = logging.getLogger('pybsd')
IF_PROPERTY = re.compile(r'^_\w*_if$')


class BaseSystem(object):
    """Describes a base OS instance, as a computer, a virtualized system or a jail

    It provides common functionality for a full system, a jail or a virtualized instance.

    Parameters
    ----------
    name : ``str``
        a name that identifies the system.
    hostname : ``Optional[int]``
        The system's hostname.

    Attributes
    ----------
    ExecutorClass : ``Executor``
        the class of the system's executor. It must be an instance of ``pybsd.systems.executors.Executor``

    """
    ExecutorClass = Executor

    def __init__(self, name, hostname=None):
        super(BaseSystem, self).__init__()
        #: ``str``: a name that identifies the system
        self.name = name
        #: ``str`` or ``None``: The system's hostname
        self.hostname = (hostname or name)
        #: ``Callable``: a method that proxies binaries invocations
        self.execute = self.ExecutorClass()


class System(BaseSystem):
    """Describes a full OS instance

    It provides common functionality for a full system, a jail or a virtualized instance.

    Each interface is described by a tuple (interface_name, [list_of_ip_interfaces]).

    Each ip interface is an ip and a prefixlen. Example:

    ('re0', ['10.0.2.0/24', '10.0.1.0/24', '1c02:4f8:0f0:14e6::2:0:1/110', '1c02:4f8:0f0:14e6::1:0:1/110'])

    Parameters
    ----------
    name : str
        a name that identifies the system.
    ext_if : Tuple(str, List[str])
        Definition of the system's outward-facing interface
    int_if : Optional[Tuple(str, List[str])]
        Definition of the system's internal network-facing interface. If it is not specified it defaults to ext_if,
        as in that case the same interface will be used for all networks.
    lo_if : Optional[Tuple(str, List[str])]
        Definition of the system's loopback interface. It defaults to ('lo0', ['127.0.0.1/8', '::1/110'])
    hostname : Optional[int]
        The system's hostname.

    Attributes
    ----------
    ExecutorClass : ``pybsd.systems.executors.Executor``
        the class of the system's executor. It must be an instance of ``pybsd.systems.executors.Executor``

    """
    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None):
        super(System, self).__init__(name=name, hostname=hostname)
        self.ext_if = ext_if
        self.int_if = int_if
        self.lo_if = lo_if

    @property
    def ext_if(self):
        """pybsd.systems.network.Interface: the system's outward-facing interface"""
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
        """pybsd.systems.network.Interface: the system's internal network-facing interface"""
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
        """pybsd.systems.network.Interface: the system's loopback interface"""
        return self._lo_if

    @lo_if.setter
    def lo_if(self, _if):
        if not _if:
            _if = ('lo0', ['127.0.0.1/8', '::1/110'])
        if_name, if_ips = _if
        _lo_if = Interface(name=if_name, ips=if_ips)
        intersec = _lo_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._lo_if = _lo_if

    @property
    def ips(self):
        """set([str]): The list of all ips in this system."""
        ips = set()
        for prop, interface in six.iteritems(self.__dict__):
            if IF_PROPERTY.match(prop) and interface:
                ips.update([x.ip.compressed for x in interface.ifsv4])
                ips.update([x.ip.compressed for x in interface.ifsv6])
        return ips
