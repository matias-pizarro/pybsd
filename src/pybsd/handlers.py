# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import unipath

from . import network
from .exceptions import MasterJailMismatchError, MissingMainIPError

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
    def derive_interface(cls, master_if, jail):
        _name = master_if.name
        ips = []
        if master_if.main_ifv4:
            prefixlen = str(master_if.main_ifv4.network.prefixlen)
            ip_chunks = master_if.main_ifv4.ip.exploded.split('.')
            ip_chunks[2] = str(jail.jail_class_id)
            ip_chunks[3] = str(jail.uid)
            _ip = '.'.join(ip_chunks)
            ip_as_string = '{}/{}'.format(_ip, prefixlen)
            ips.append(ip_as_string)
        if master_if.main_ifv6:
            prefixlen = str(master_if.main_ifv6.network.prefixlen)
            ip_chunks = master_if.main_ifv6.ip.exploded.split(':')
            ip_chunks[5] = str(jail.jail_class_id)
            ip_chunks[6] = str(jail.uid)
            ip_chunks[7] = '1'
            _ip = ':'.join(ip_chunks)
            ipv6_as_string = '{}/{}'.format(_ip, prefixlen)
            ips.append(ipv6_as_string)
        if not len(ips):
            raise MissingMainIPError(jail.master, master_if)
        return network.Interface(_name, ips)

    def check_mismatch(self, jail):
        if jail.master != self.master:
            raise MasterJailMismatchError(self.master, jail)

    def get_jail_type(self, jail):
        # provides a mechanism to decide jail type
        self.check_mismatch(jail)
        return self.master.default_jail_type

    def get_jail_hostname(self, jail, strict=True):
        if strict:
            self.check_mismatch(jail)
        return '{}.{}'.format(jail.name, self.master.hostname)

    def get_jail_path(self, jail):
        self.check_mismatch(jail)
        return self.jail_root.child(jail.name)

    def get_jail_ext_if(self, jail):
        """Returns a given jail's ext_if

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose ext_if is requested

        Returns
        -------
        : :py:class:`~pybsd.network.Interface`
            the jail's ext_if
        """
        self.check_mismatch(jail)
        return self.derive_interface(self.master.j_if, jail=jail)

    def get_jail_lo_if(self, jail):
        """Returns a given jail's lo_if

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose lo_if is requested

        Returns
        -------
        : :py:class:`~pybsd.network.Interface`
            the jail's lo_if
        """
        self.check_mismatch(jail)
        return self.derive_interface(self.master.jlo_if, jail=jail)
