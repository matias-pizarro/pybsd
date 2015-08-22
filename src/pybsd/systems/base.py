# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
import re
import six
import sortedcontainers
from ..executors import Executor
from ..network import Interface

__logger__ = logging.getLogger('pybsd')
IF_PROPERTY = re.compile(r'^_\w*_if$')


class BaseSystem(object):
    """Describes a base OS instance such as a computer, a virtualized system or a jail

    It provides common functionality for a full system, a jail or a virtualized instance.
    This allows interaction with both real and modelized instances.

    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the system.
    hostname : Optional[:py:class:`str`]
        The system's hostname. If not specified, the system's name is used instead.

    Attributes
    ----------
    ExecutorClass : :py:class:`class`
        the class of the system's executor. It must be or extend :py:class:`~pybsd.Executor`
    """
    ExecutorClass = Executor

    def __init__(self, name, hostname=None):
        super(BaseSystem, self).__init__()
        #: :py:class:`str`: a name that identifies the system
        self.name = name
        #: :py:class:`str` or :py:class:`~None`: The system's hostname
        self.hostname = (hostname or name)
        #: :py:class:`~function`: a method that proxies binaries invocations
        self.execute = self.ExecutorClass()


class System(BaseSystem):
    """Describes a full OS instance

    It provides common functionality for a full system.

    Each interface is described by:

        :py:class:`tuple` (interface_name (:py:class:`str`), :py:class:`list` [ip_interfaces (:py:class:`str`)]).

    Each ip interface is composed of an ip and an optional prefixlen, such as::

    ('re0', ['10.0.2.0/24', '10.0.1.0/24', '1c02:4f8:0f0:14e6::2:0:1/110', '1c02:4f8:0f0:14e6::1:0:1/110'])

    if the prefixlen is not specified it will default to /32 (IPv4) or /128 (IPv6)

    Example
    -------

    >>> from pybsd import System
    >>> box01 = System(name='box01',
    ...                hostname='box01.foo.bar',
    ...                ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
    ...                int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']))
    >>> '148.241.178.106' in box01.ips
    True
    >>> '148.241.178.101' in box01.ips
    False
    >>> box01.ips
    SortedSet(['127.0.0.1', '148.241.178.106', '192.168.0.0', '1c02:4f8:f0:14e6::', '1c02:4f8:f0:14e6::1', '::1'], key=None, load=1000)


    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the system.
    ext_if : :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`])
        Definition of the system's outward-facing interface
    int_if : Optional[ :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`]) ]
        Definition of the system's internal network-facing interface. If it is not specified it defaults to ext_if,
        as in that case the same interface will be used for all networks.
    lo_if : Optional[ :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`]) ]
        Definition of the system's loopback interface. It defaults to ('lo0', ['127.0.0.1/8', '::1/110'])
    hostname : Optional[:py:class:`int`]
        The system's hostname.
    """
    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None):
        super(System, self).__init__(name=name, hostname=hostname)
        self.ext_if = ext_if
        self._int_if = None
        if int_if:
            self.int_if = int_if
        self.lo_if = lo_if

    @property
    def ext_if(self):
        """:py:class:`~pybsd.Interface`: the system's outward-facing interface"""
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
        """:py:class:`~pybsd.Interface`: the system's internal network-facing interface"""
        return self._int_if or self.ext_if

    @int_if.setter
    def int_if(self, _if):
        if_name, if_ips = _if
        _int_if = Interface(name=if_name, ips=if_ips)
        intersec = _int_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._int_if = _int_if

    @property
    def lo_if(self):
        """:py:class:`~pybsd.Interface`: the system's loopback interface"""
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
        """:py:class:`set` ([ :py:class:`str` ]): The list of all ips in this system."""
        ips = sortedcontainers.SortedSet()
        for prop, interface in six.iteritems(self.__dict__):
            if IF_PROPERTY.match(prop) and interface:
                ips.update([x.ip.compressed for x in interface.ifsv4])
                ips.update([x.ip.compressed for x in interface.ifsv6])
        return ips
