# -*- coding: utf-8 -*-
"""The :py:mod:`~pybsd.systems.jails` module provides classes which are used to represent jail
instances. When attached to a master a jail can be created, deleted and controlled through said
master's ezjail-admin interface.

Example
--------
::

    from pybsd.systems.jails import Jail
    from pybsd.systems.masters import Master
    master01 = Master(name='master01',
                      hostname='master01.foo.bar',
                      ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
                      int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']),
                      j_if=('re0', ['10.0.1.0/24', '1c02:4f8:0f0:14e6::1:0:1/110']),
                      jlo_if=('lo1', ['127.0.1.0/24', '::0:1:0:0/110']))
    jail01 = Jail(name='system',
                  uid=12,
                  hostname='system.foo.bar',
                  master=None,
                  jail_type='Z',
                  auto_start=True,
                  jail_class='web')


Classes
-------
"""
from __future__ import unicode_literals, print_function, absolute_import
import six
import logging
from . import BaseSystem

__logger__ = logging.getLogger('pybsd')


class Jail(BaseSystem):
    """Describes a jailed system

    Possible types are:
        * **D** --> Directory tree based jail.
        * **I** --> File-based jail.
        * **E** --> Geli encrypted file-based jail.
        * **B** --> Bde encrypted file-based jail.
        * **Z** --> ZFS filesystem-based jail.

    """

    def __init__(self, name, uid, hostname=None, master=None, jail_type=None, auto_start=False, jail_class='service'):
        super(Jail, self).__init__(name=name, hostname=hostname)
        self.uid = uid
        self.jail_type = jail_type
        self.auto_start = auto_start
        self.jail_class = jail_class
        self.master = None
        if master:
            try:
                master.add_jail(self)
            except AttributeError:
                raise SystemError('`{}` is not a jail master'.format(master.name))

    @property
    def status(self):
        return getattr(self, '_status', 'S')

    @status.setter
    def status(self, _status):
        """
        Here we shall later hook polling of real jails if applicable

        Possible status
        R     The jail is running.
        A     The image of the jail is mounted, but the jail is not running.
        S     The jail is stopped.
        """
        if _status not in 'RAS':
            raise SystemError('`{}` is not a valid status (it must be one of R, A or S)'.format(_status))
        self._status = _status

    @property
    def jid(self):
        return getattr(self, '_jid', None)

    @jid.setter
    def jid(self, _jid):
        """ Here we shall later hook polling of real jails if applicable"""
        if not isinstance(_jid, six.integer_types):
            raise SystemError('`{}` is not a valid jid (it must be an integer)'.format(_jid))
        self._jid = _jid

    @property
    def jail_class_id(self):
        return self.master.jail_handler.jail_class_ids[self.jail_class]

    @property
    def path(self):
        if self.master:
            return self.master.jail_handler.get_jail_path(self)
        return None

    @property
    def ext_if(self):
        if self.master:
            return self.master.jail_handler.get_jail_ext_if(self)
        return None

    @ext_if.setter
    def ext_if(self, _if):
        raise SystemError('Jail interfaces cannot be directly set')

    @property
    def lo_if(self):
        if self.master:
            return self.master.jail_handler.get_jail_lo_if(self)
        return None

    @lo_if.setter
    def lo_if(self, _if):
        raise SystemError('Jail interfaces cannot be directly set')
