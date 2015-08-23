# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
from .base import BaseSystem

__logger__ = logging.getLogger('pybsd')


class Jail(BaseSystem):
    """Describes a jailed system

    When attached to an instance of :py:class:`~pybsd.Master` a jail can be created, deleted and controlled through said master's
    ezjail-admin interface.

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
    ...               jail_type='Z',
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
    master : Optional[:py:class:`~pybsd.Master`]
        The jail's master i.e. host system. Default is None
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
    SystemError
        if `master` is specified and is not an instance of :py:class:`~pybsd.Master`
    """

    def __init__(self, name, uid, hostname=None, master=None, jail_type=None, auto_start=False, jail_class='service'):
        super(Jail, self).__init__(name=name, hostname=hostname)
        #: :py:class:`int`: The jail's id, unique over a user's or an organization's domain
        self.uid = uid
        #: Optional[:py:class:`str`]: The jail's type, according to its storage solution.
        self.jail_type = jail_type
        #: Optional[:py:class:`bool`]: Whether the jail should be started automatically at host system's boot time.
        self.auto_start = auto_start
        #: Optional[:py:class:`str`]: Allows differentiating jails by class.
        self.jail_class = jail_class
        #: Optional[:py:class:`~pybsd.Master`]: The jail's master i.e. host system. By default a :py:class:`~pybsd.Jail` is created
        #: detached.
        self.master = None
        if master:
            try:
                master.add_jail(self)
            except AttributeError:
                raise SystemError('`{}` is not a jail master'.format(master.name))

    @property
    def is_attached(self):
        """:py:class:`bool`: Whether the jail is currently attached to a master."""
        return self.master is not None

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
            return self.master.jail_handler.jail_class_ids[self.jail_class]
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
            return self.master.jail_handler.get_jail_path(self)
        else:
            return None

    @property
    def ext_if(self):
        """:py:class:`~pybsd.Interface`: the jail's outward-facing interface. It is evaluated dynamically by the
        master's jail handler, so that the same base jail cloned on different host systems can return different values.
        """
        if self.is_attached:
            return self.master.jail_handler.get_jail_ext_if(self)
        else:
            return None

    @property
    def lo_if(self):
        """:py:class:`~pybsd.Interface`: the jail's loopback interface. It is evaluated dynamically by the
        master's jail handler, so that the same base jail cloned on different host systems can return different values.
        """
        if self.is_attached:
            return self.master.jail_handler.get_jail_lo_if(self)
        else:
            return None
