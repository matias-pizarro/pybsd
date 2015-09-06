# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import unipath

from . import network
from .exceptions import InvalidMainIPError, MasterJailMismatchError, MissingMainIPError
from .utils import from_split_if, split_if

__logger__ = logging.getLogger('pybsd')


class BaseJailHandler(object):
    """Provides a base jail handler

    Handlers allow custom parametrization and customization of all logic pertaining to the jails. Each aspect of the handling is
    delegated to a method that can be called from the master or the jail.

    Parameters
    ----------
    master : Optional[:py:class:`~pybsd.systems.masters.Master`]
        The handler's master.
    jail_root : :py:class:`str`
        the path on the host's filesystem to the jails directory that the handler will enforce

    Attributes
    ----------
    default_jail_root : :py:class:`str`
        the default jail_root.
    jail_class_ids : :py:class:`dict`
        a dictionary linking jail class types and the numerical ids that are to be linked to them by this handler.

    Raises
    ------
    MissingMainIPError
        when a master's interface does not define a main_if
    InvalidMainIPError
        when a master's main_if violates established rules
    MasterJailMismatchError
        if a `master` and a `jail` called in a method are not related
    """
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
        """Derives a jail's :py:class:`~pybsd.network.Interface` based on the handler's master's

        Parameters
        ----------
        master_if : :py:class:`~pybsd.systems.jails.Jail`
            master's :py:class:`~pybsd.network.Interface` to which the jail's is attched
        jail : :py:class:`~pybsd.network.Interface`
            the jail whose :py:class:`~pybsd.network.Interface` is requested

        Returns
        -------
        : :py:class:`~pybsd.network.Interface`
            the jail's :py:class:`~pybsd.network.Interface`

        Raises
        ------
        MissingMainIPError
            when a master's interface does not define a main_if
        InvalidMainIPError
            when a master's main_if violates established rules
        """
        if master_if.main_ifv4 or master_if.main_ifv6:
            _if = network.Interface(master_if.name)
            if master_if.main_ifv4:
                ip_chunks = split_if(master_if.main_ifv4)
                if int(ip_chunks[-1]) != 0:
                    raise InvalidMainIPError(jail.master, master_if, "an IPv4 main_ip's last octet must be equal to 0")
                ip_chunks[4] = str(jail.jail_class_id)
                ip_chunks[5] = str(jail.uid)
                _ip = from_split_if(ip_chunks)
                _if.add_ips(_ip)
            if master_if.main_ifv6:
                ip_chunks = split_if(master_if.main_ifv6)
                if int(ip_chunks[-2]) != 0:
                    raise InvalidMainIPError(jail.master, master_if, "an IPv6 main_ip's penultimate octet must be equal to 0")
                ip_chunks[7] = str(jail.jail_class_id)
                ip_chunks[8] = str(jail.uid)
                ip_chunks[9] = '1'
                _ip = from_split_if(ip_chunks)
                _if.add_ips(_ip)
            return _if
        else:
            raise MissingMainIPError(jail.master, master_if)

    def check_mismatch(self, jail):
        """Checks whether a given jail belongs to the handler's master

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose status is checked

        Returns
        -------
        : :py:class:`bool`
            whether the jail belongs to the handler's master

        Raises
        ------
        MasterJailMismatchError
            if a `master` and a `jail` called in a method are not related
        """
        if jail.master != self.master:
            raise MasterJailMismatchError(self.master, jail)

    def get_jail_type(self, jail):
        """Returns a given jail's type.

        The default implementation simply honours the master's default jail type and provides an esaily overridable method
        where custom logic can be applied.

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose jail type is requested

        Returns
        -------
        : :py:class:`str`
            the jail's type. For base values see :py:meth:`~pybsd.systems.jails.Jail.jail_type`
        """
        self.check_mismatch(jail)
        return self.master.default_jail_type

    def get_jail_hostname(self, jail, strict=True):
        """Returns a given jail's hostname.

        if strict is set to `False`, it will evaluate what the jail hostname would be if it were attached to the handler's master.

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose hostname is requested
        strict : Optional[ :py:class:`bool` ]
            whether the handler should only return hostnames for jails attached to its master. Default is `True`.

        Returns
        -------
        : :py:class:`unipath.Path`
            the jail's path
        """
        if strict:
            self.check_mismatch(jail)
        return '{}.{}'.format(jail.name, self.master.hostname)

    def get_jail_path(self, jail):
        """Returns a given jail's path

        Parameters
        ----------
        jail : :py:class:`~pybsd.systems.jails.Jail`
            the jail whose path is requested

        Returns
        -------
        : :py:class:`unipath.Path`
            the jail's path
        """
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
