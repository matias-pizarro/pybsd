# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import ipaddress
import six
import sortedcontainers

__logger__ = logging.getLogger('pybsd')


class Interface(object):
    """Describes a network interface

    An interface has main :py:class:`ipaddress.IPv4Interface` and a main :py:class:`ipaddress.IPv6Interface`.
    Any other :py:class:`ipaddress.IPvxInterface` will be added as an alias. Main addresses as used by the default
    :py:class:`~pybsd.handlers.BaseJailHandler` as the basis to calculate jail interfaces
    (see :py:class:`~pybsd.handlers.BaseJailHandler.derive_interface`).
    Interfaces can be checked for equality based on their name and list of ips.

    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the interface.
    ips : Optional[ :py:class:`str`, :py:class:`list`[:py:class:`str`] or :py:class:`set`(:py:class:`str`) ]
        a single ip address or a list of ip addresses, represented as strings. Duplicates are silently ignored.
        The first ip added for each version will become the main ip address for this interface.
    """
    def __init__(self, name, ips=None):
        #: :py:class:`str`: a name that identifies the interface.
        self.name = name
        #: :py:class:`sortedcontainers.SortedSet` ([ :py:class:`ipaddress.IPv4Interface` ]): a sorted set containing all the
        #: IPv4 interfaces on this physical interface.
        self.ifsv4 = sortedcontainers.SortedListWithKey(key=lambda x: x.ip.compressed)
        #: :py:class:`sortedcontainers.SortedSet` ([ :py:class:`ipaddress.IPv6Interface` ]): a sorted set containing all the
        #: IPv6 interfaces on this physical interface.
        self.ifsv6 = sortedcontainers.SortedListWithKey(key=lambda x: x.ip.compressed)
        #: :py:class:`ipaddress.IPv4Interface`: this interface's main IPv4 interface
        self.main_ifv4 = None
        #: :py:class:`ipaddress.IPv6Interface`: this interface's main IPv6 interface
        self.main_ifv6 = None
        ips = ips or []
        self.add_ips(ips)

    def add_ips(self, ips):
        """Adds a single ip address or a list of ip addresses, represented as strings, to the interface.

        None and duplicates are silently ignored.

        Parameters
        ----------
        ips : :py:class:`str`, :py:class:`list`[:py:class:`str`] or :py:class:`set`(:py:class:`str`)
            a single ip address or a list of ip addresses, represented as strings. Duplicates are silently ignored.
            The first ip added for each version will become the main ip address for this interface.
        """
        if ips:
            if isinstance(ips, six.string_types):
                ips = [ips]
            for _ip in ips:
                _if = ipaddress.ip_interface(_ip)
                if _if.ip.compressed not in self.ips:
                    if _if.version == 4:
                        self.ifsv4.add(_if)
                        if len(self.ifsv4) == 1:
                            self.main_ifv4 = _if
                    else:
                        self.ifsv6.add(_if)
                        if len(self.ifsv6) == 1:
                            self.main_ifv6 = _if

    @property
    def ips(self):
        """:py:class:`sortedcontainers.SortedSet` ([ :py:class:`str` ]): a sorted set containing all ips on this interface."""
        ips = sortedcontainers.SortedSet()
        return ips.update({x.ip.compressed for x in self.ifsv4 + self.ifsv6})

    def __eq__(self, other):
        """Compares interface based on their name, and list of ips"""
        name_eq = self.name == other.name
        ifsv4_eq = self.ifsv4 == other.ifsv4
        ifsv6_eq = self.ifsv6 == other.ifsv6
        return name_eq and ifsv4_eq and ifsv6_eq

    @property
    def alias_ifsv4(self):
        """:py:class:`sortedcontainers.SortedSet` ([ :py:class:`ipaddress.IPv4Interface` ]): a sorted set containing this \
        interface's IPv4 aliases"""
        ifs = self.ifsv4.copy()
        ifs.remove(self.main_ifv4)
        return ifs

    @property
    def alias_ifsv6(self):
        """:py:class:`sortedcontainers.SortedSet` ([ :py:class:`ipaddress.IPv4Interface` ]): a sorted set containing this \
        interface's IPv6 aliases"""
        ifs = self.ifsv6.copy()
        ifs.remove(self.main_ifv6)
        return ifs

    def __repr__(self):
        # Maps the interface's string representation to its name
        #
        # Returns
        # -------
        # : :py:class:`str`
        #     the interface's name
        return self.name
