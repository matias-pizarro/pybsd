# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import ipaddress
import six
import sortedcontainers

__logger__ = logging.getLogger('pybsd')


class Interface(object):
    """Describes a network interface"""
    def __init__(self, name, ips):
        self.name = name
        self.ifsv4 = sortedcontainers.SortedListWithKey(key=lambda x: x.ip.compressed)
        self.ifsv6 = sortedcontainers.SortedListWithKey(key=lambda x: x.ip.compressed)
        self.add_ips(ips)

    def add_ips(self, ips):
        if isinstance(ips, six.string_types):
            ips = [ips]
        for _ip in ips:
            _if = ipaddress.ip_interface(_ip)
            if _if.ip.compressed not in self.ips:
                if _if.version == 4:
                    self.ifsv4.add(_if)
                else:
                    self.ifsv6.add(_if)

    @property
    def ips(self):
        ips = set()
        ips.update([x.ip.compressed for x in self.ifsv4])
        ips.update([x.ip.compressed for x in self.ifsv6])
        return ips

    def __eq__(self, other):
        name_eq = self.name == other.name
        ifsv4_eq = self.ifsv4 == other.ifsv4
        ifsv6_eq = self.ifsv6 == other.ifsv6
        return name_eq and ifsv4_eq and ifsv6_eq

    @property
    def main_ifv4(self):
        return self.ifsv4[0] if len(self.ifsv4) else None

    @property
    def alias_ifsv4(self):
        return self.ifsv4[1:]

    @property
    def main_ifv6(self):
        return self.ifsv6[0] if len(self.ifsv6) else None

    @property
    def alias_ifsv6(self):
        return self.ifsv6[1:]

    def __repr__(self):
        # Maps the interface's string representation to its name
        #
        # Returns
        # -------
        # : :py:class:`str`
        #     the interface's name
        return self.name
