# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import logging
from . import BaseSystem, SystemError


__logger__ = logging.getLogger('pybsd')


class Jail(BaseSystem):
    """Describes a jailed system"""

    def __init__(self, name, uid, hostname=None, master=None, jail_type=None, auto_start=False):
        super(Jail, self).__init__(name=name, hostname=hostname)
        """
        Possible types
        D     Directory tree based jail.
        I     File-based jail.
        E     Geli encrypted file-based jail.
        B     Bde encrypted file-based jail.
        Z     ZFS filesystem-based jail.
        """
        self.uid = uid
        self.jail_type = jail_type
        self.auto_start = auto_start
        """
        if master:
            if name in master.jails:
                raise SystemError('a jail called `{}` is already attached to `{}`'.format(name, master.name))
            if uid in master.uids:
                raise SystemError('a jail with id `{}` is already attached to `{}`'.format(id, master.name))
            master.add_jail(self)
        """

    @property
    def status(self):
        return getattr(self, '_status', 'S')

    @status.setter
    def status(self, _status):
        """ Here we shall later hook polling of real jails if applicable"""
        """
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
