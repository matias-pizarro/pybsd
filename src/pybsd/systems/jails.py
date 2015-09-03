# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

from ..exceptions import AttachNonMasterError, DuplicateJailHostnameError, DuplicateJailNameError, DuplicateJailUidError
from .base import BaseSystem

__logger__ = logging.getLogger('pybsd')


class Jail(BaseSystem):
    """Describes a jailed system

    When attached to an instance of :py:class:`~pybsd.systems.masters.Master` a jail can be created, deleted
    and controlled through said master's ezjail-admin interface.

    Example
    -------

    >>> from pybsd import Jail, Master
    >>> master01 = Master(name='master01',
    ...                   hostname='master01.foo.bar',
    ...                   ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
    ...                   int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']),
    ...                   j_if=('re0', ['10.0.1.0/24', '1c02:4f8:0f0:14e6::1:0:1/110']),
    ...                   jlo_if=('lo1', ['127.0.1.0/24', '::0:1:0:0/110']))
    >>> jail01 = Jail(name='system',
    ...               uid=12,
    ...               hostname='system.foo.bar',
    ...               master=None,
    ...               auto_start=True,
    ...               jail_class='web')


    Parameters
    ----------
    name : :py:class:`str`
        a name that identifies the jail.
    uid : :py:class:`int`
        The jail's id, unique over a user's or an organization's domain.
    hostname : Optional[:py:class:`str`]
        The jail's hostname. It not specified the jail's name is used instead.
        #: Optional[:py:class:`~pybsd.systems.masters.Master`]:
    master : Optional[:py:class:`~pybsd.systems.masters.Master`]
        The jail's master i.e. host system. By default a :py:class:`~pybsd.systems.jails.Jail` is created detached and the value
        of master is None.
    jail_type : Optional[:py:class:`str`]
        The jail's type, according to its storage solution.
        If the jail is not attached it is set to None by default.
        If attached the default is `Z`, for ZFS filesystem-based jail.

        Possible types are:
            * **D** --> Directory tree based jail.
            * **I** --> File-based jail.
            * **E** --> Geli encrypted file-based jail.
            * **B** --> Bde encrypted file-based jail.
            * **Z** --> ZFS filesystem-based jail.
    auto_start : Optional[:py:class:`bool`]
        Whether the jail should be started automatically at host system's boot time.
    jail_class : Optional[:py:class:`str`]
        Allows differentiating jails by class. This will be worked out of base jails to depend on the jail handler. The
        base handler will probably not have the notion of classes

    Raises
    ------
    AttachNonMasterError
        if `master` is specified and is not an instance of :py:class:`~pybsd.systems.masters.Master`
    DuplicateJailNameError
        if `master` is specified and the jail's name is already attached to it
    DuplicateJailHostnameError
        if `master` is specified and the jail's hostname is already attached to it
    DuplicateJailUidError
        if `master` is specified and the jail's uid is already attached to it
    JailAlreadyAttachedError
        if `master` is specified and the jail is already attached to another master
    """

    def __init__(self, name, uid, hostname=None, master=None, auto_start=False, jail_class='service'):
        super(Jail, self).__init__(name=name, hostname=hostname)
        self._uid = uid
        self.auto_start = auto_start
        self.jail_class = jail_class
        self.master = None
        if master:
            try:
                master.attach_jail(self)
            except AttributeError:
                raise AttachNonMasterError(master, self)

    @property
    def is_attached(self):
        """:py:class:`bool`: Whether the jail is currently attached to a master."""
        return self.master is not None

    @property
    def handler(self):
        """:py:class:`bool`: Whether the jail is currently attached to a master."""
        return self.master.jail_handler if self.is_attached else None

    @property
    def name(self):
        """:py:class:`str`: a name that identifies the system."""
        return self._name

    @name.setter
    def name(self, name):
        if self.is_attached:
            if name in self.master.names:
                raise DuplicateJailNameError(self.master, self, name)
        self._name = name

    @property
    def base_hostname(self):
        """:py:class:`str` or :py:class:`NoneType`: The system's hostname."""
        return self._hostname

    @property
    def hostname(self):
        """:py:class:`str` or :py:class:`NoneType`: The jail's hostname. If not attached, it. is equal to None"""
        if self.is_attached:
            return self._hostname or self.handler.get_jail_hostname(self)
        else:
            return None

    @hostname.setter
    def hostname(self, hostname):
        if self.is_attached:
            if hostname in self.master.hostnames:
                raise DuplicateJailHostnameError(self.master, self, hostname)
        self._hostname = hostname

    @property
    def uid(self):
        """:py:class:`int`: The jail's uid."""
        return self._uid

    @uid.setter
    def uid(self, uid):
        if self.is_attached:
            if uid in self.master.uids:
                raise DuplicateJailUidError(self.master, self, uid)
        self._uid = uid

    @property
    def jail_type(self):
        """:py:class:`str` or :py:class:`NoneType`: The jail's type, according to its storage solution.
        If not attached, it. is equal to None"""
        return self.handler.get_jail_type(self) if self.is_attached else None

    @property
    def status(self):
        """:py:class:`str`: Returns this jail's status as per ezjail_admin

        Possible status
            * **D**     The jail is detached (not attached to any master)
            * **S**     The jail is stopped.
            * **A**     The image of the jail is mounted, but the jail is not running.
            * **R**     The jail is running.

        The `S` value is a stub for now. It must come from parsing master's ezjail-admin.list()'s output
        """
        if self.is_attached:
            return 'S'
        else:
            return 'D'

    @property
    def jid(self):
        """:py:class:`int`: Returns this jail's jid as per ezjail_admin

        The `1` value returned when attached is a stub for now. It must come from parsing master's
        ezjail-admin.list()'s output
        """
        if self.is_attached:
            return 1
        else:
            return None

    @property
    def jail_class_id(self):
        """:py:class:`int`: Returns this jail's class id.

        This is an integer value which is given by its jail_handler according to its class.
        """
        if self.is_attached:
            return self.handler.jail_class_ids[self.jail_class]
        else:
            return None

    @property
    def path(self):
        """:py:class:`unipath.Path`: the absolute path of the jail's filesystem, relative to the host's filesystem. It is evaluated
        dynamically by the master's jail handler, so that the same base jail cloned on different host systems can return
        different values. By default it resolves to a directory called after jail.name, inside the host system's
        jail_path: foo.path = unipath.Path('/usr/jails/foo').
        """
        if self.is_attached:
            return self.handler.get_jail_path(self)
        else:
            return None

    @property
    def ext_if(self):
        """:py:class:`~pybsd.network.Interface`: the jail's outward-facing interface. It is evaluated dynamically by the
        master's jail handler, so that the same base jail cloned on different host systems can return different values.
        """
        if self.is_attached:
            return self.handler.get_jail_ext_if(self)
        else:
            return None

    @property
    def lo_if(self):
        """:py:class:`~pybsd.network.Interface`: the jail's loopback interface. It is evaluated dynamically by the
        master's jail handler, so that the same base jail cloned on different host systems can return different values.
        """
        if self.is_attached:
            return self.handler.get_jail_lo_if(self)
        else:
            return None
