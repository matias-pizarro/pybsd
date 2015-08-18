# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import copy
from lazy import lazy
import logging
import six
from ..commands.ezjail_admin import EzjailAdmin
from ..handlers import BaseJailHandler
from ..network import Interface
from . import System
from .jails import Jail

__logger__ = logging.getLogger('pybsd')


class Master(System):
    """Describes a system that will host jails"""
    JailHandlerClass = BaseJailHandler
    default_jail_type = 'Z'

    def __init__(self, name, ext_if, int_if=None, lo_if=None, j_if=None, jlo_if=None, hostname=None):
        super(Master, self).__init__(name, ext_if, int_if, lo_if, hostname)
        self._j_if = None
        if j_if:
            self.j_if = j_if
        self._jlo_if = None
        if jlo_if:
            self.jlo_if = jlo_if
        self.ezjail_admin = EzjailAdmin(env=self)
        self.jail_handler = self.JailHandlerClass(master=self)
        self.jails = {}

    @property
    def j_if(self):
        """
        By default, a master uses its own ext_if as jails ext_if
        """
        return self._j_if or self.ext_if

    @j_if.setter
    def j_if(self, _if):
        if_name, if_ips = _if
        _j_if = Interface(name=if_name, ips=if_ips)
        intersec = _j_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        else:
            self._j_if = _j_if

    def reset_j_if(self):
        self._j_if = None

    @property
    def jlo_if(self):
        return self._jlo_if or self.lo_if

    @jlo_if.setter
    def jlo_if(self, _if):
        if_name, if_ips = _if
        _jlo_if = Interface(name=if_name, ips=if_ips)
        intersec = _jlo_if.ips.intersection(self.ips)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        else:
            self._jlo_if = _jlo_if

    def reset_jlo_if(self):
        self._jlo_if = None

    def add_jail(self, jail):
        if not isinstance(jail, Jail):
            raise SystemError(u'`{}` should be an instance of systems.Jail'.format(jail.name))
        if jail.master:
            if jail.master == self:
                return jail
            raise SystemError('Jail `{}` is already attached to `{}`'.format(jail.name, jail.master.name))
        if jail.name in self.jails:
            raise SystemError('a jail called `{}` is already attached to `{}`'.format(jail.name, self.name))
        if jail.uid in self.uids:
            raise SystemError('a jail with uid `{}` is already attached to `{}`'.format(jail.uid, self.name))
        self.jails[jail.name] = jail
        jail.master = self
        jail.jail_type = jail.jail_type or self.default_jail_type
        return jail

    @property
    def uids(self):
        return [j.uid for k, j in six.iteritems(self.jails)]

    def clone_jail(self, jail, name, uid):
        _jail = copy.deepcopy(jail)
        _jail.name = name
        _jail.uid = uid
        _jail.master = None
        return self.add_jail(_jail)

    @lazy
    def ezjail_admin_binary(self):
        return u'/usr/local/bin/ezjail-admin'
