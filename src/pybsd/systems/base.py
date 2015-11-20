# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import re

import six
import sortedcontainers

from ..exceptions import DuplicateIPError
from ..executors import Executor
from ..network import Interface

__logger__ = logging.getLogger('pybsd')
IF_PROPERTY = re.compile(r'^\w*_if$')


class BaseSystem(object):
    """Describes a base OS instance such as a computer, a virtualized system or a jail

    It provides common functionality for a full system, a jail or a virtualized instance.
    This allows interaction with both real and modelized instances.

    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the system.
    hostname : Optional[:py:class:`str`]
        The system's hostname.

    Attributes
    ----------
    ExecutorClass : :py:class:`class`
        the class of the system's executor. It must be or extend :py:class:`~pybsd.executors.Executor`
    """
    ExecutorClass = Executor

    def __init__(self, name, hostname=None):
        super(BaseSystem, self).__init__()
        self._name = name
        self._hostname = hostname
        #: :py:class:`~function`: a method that proxies binaries invocations
        self.execute = self.ExecutorClass()

    @property
    def name(self):
        """:py:class:`str`: a name that identifies the system."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def hostname(self):
        """:py:class:`str`: The system's hostname. If not specified, the system's name is returned instead."""
        return self._hostname or self.name

    @hostname.setter
    def hostname(self, hostname):
        self._hostname = hostname

    def __repr__(self):
        # Maps the system's string representation to its hostname
        #
        # Returns
        # -------
        # : :py:class:`str`
        #     the system's hostname
        return self.name


class System(BaseSystem):
    """Describes a full OS instance

    It provides common functionality for a full system.

    **Interfaces**

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
    ...                ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110', '1c02:4f8:000:14e6::/110']),
    ...                int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110'])
    ...               )
    >>> '148.241.178.106' in box01.ips
    True
    >>> '148.241.178.101' in box01.ips
    False
    >>> box01.ips
    SortedSet(['127.0.0.1', '148.241.178.106', '192.168.0.0', '1c02:4f8:0:14e6::', '1c02:4f8:f0:14e6::', '1c02:4f8:f0:14e6::1', \
'::1'], key=None, load=1000)

    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the system.
    ext_if : :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`])
        Interface definition used to initialize self.ext_if
    int_if : Optional[ :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`]) ]
        Interface definition used to initialize self.int_if
    lo_if : Optional[ :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`]) ]
        Interface definition used to initialize self.lo_if
    hostname : Optional[:py:class:`int`]
        The system's hostname.

    Raises
    ------
    DuplicateIPError
        if any ip address in the interface definitions is already in use.
    """
    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None):
        super(System, self).__init__(name=name, hostname=hostname)
        #: :py:class:`~pybsd.network.Interface`: the system's outward-facing interface
        self.ext_if = self.make_if(ext_if)
        self._int_if = self.make_if(int_if)
        lo_if = lo_if or ('lo0', ['127.0.0.1/8', '::1/110'])
        #: :py:class:`~pybsd.network.Interface`: the system's loopback interface. If not expressly defined, it defaults to
        #: ('lo0', ['127.0.0.1/8', '::1/110'])
        self.lo_if = self.make_if(lo_if)

    def make_if(self, definition):
        """Returns an :py:class:`~pybsd.network.Interface` based on `definition`

        Parameters
        ----------
        definition : :py:class:`tuple` (:py:class:`str`, :py:class:`list` [:py:class:`str`])

        Returns
        -------
        : :py:class:`~pybsd.network.Interface`
            a valid interface

        Raises
        ------
        DuplicateIPError
            raised if one of the ip addresses in `definition` is already in use
        """
        if not definition:
            return None
        if_name, if_ips = definition
        _if = Interface(name=if_name, ips=if_ips)
        intersec = _if.ips.intersection(self.ips)
        if len(intersec):
            raise DuplicateIPError(self, _if, intersec)
        return _if

    @property
    def int_if(self):
        """:py:class:`~pybsd.network.Interface`: the system's internal network-facing interface. If not expressly defined, it defaults to
        self.ext_if, as in that case the same interface will be used for all networks."""
        return self._int_if or self.ext_if

    def reset_int_if(self):
        """Resets the system's int_if to its default value (its own ext_if)"""
        self._int_if = None

    @property
    def interfaces(self):
        """:py:class:`dict` ([ :py:class:`~pybsd.network.Interface` ]): a list containing all interfaces on this system."""
        ifs = {}
        for prop, interface in six.iteritems(self.__dict__):
            if IF_PROPERTY.match(prop) and interface:
                ifs[interface.name] = interface
        return ifs

    @property
    def ips(self):
        """:py:class:`sortedcontainers.SortedSet` ([ :py:class:`str` ]): a sorted set containing all ips on this system."""
        ips = sortedcontainers.SortedSet()
        for interface in six.itervalues(self.interfaces):
            ips.update([x.ip.compressed for x in interface.ifsv4 + interface.ifsv6])
        return ips
