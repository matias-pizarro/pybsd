# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import copy
from lazy import lazy
import logging
from . import System, SystemError
from .commands.ezjail_admin import EzjailAdmin
from .executors import DummyExecutor
from .handlers import BaseJailHandler
from .jails import Jail
from .network import Interface


__logger__ = logging.getLogger('pybsd')


class Master(System):
    """Describes a system that will host jails"""
    _JailHandlerClass = BaseJailHandler

    def __init__(self, name, ext_if, int_if=None, lo_if=None, j_if=None, jlo_if=None, hostname=None):
        super(Master, self).__init__(name, ext_if, int_if, lo_if, hostname)
        self.j_if = j_if
        self.jlo_if = jlo_if
        self.ezjail_admin = EzjailAdmin(env=self)
        self.jail_handler = self._JailHandlerClass(master=self)
        self.jails = {}

    @property
    def j_if(self):
        """
        By default, a master uses its own ext_if as jails ext_if
        """
        return self._j_if or self.ext_if

    @j_if.setter
    def j_if(self, _if):
        if _if:
            if_name, if_ips = _if
            _j_if = Interface(name=if_name, ips=if_ips)
            intersec = _j_if.ips.intersection(self.ips)
            if len(intersec):
                raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _j_if != self.ext_if:
                self._j_if = _j_if
        else:
            self._j_if = None

    @property
    def jlo_if(self):
        return self._jlo_if or self.lo_if

    @jlo_if.setter
    def jlo_if(self, _if):
        if _if:
            if_name, if_ips = _if
            _jlo_if = Interface(name=if_name, ips=if_ips)
            intersec = _jlo_if.ips.intersection(self.ips)
            if len(intersec):
                raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _jlo_if != self.lo_if:
                self._jlo_if = _jlo_if
        else:
            self._jlo_if = None

    def add_jail(self, jail):
        if not isinstance(jail, Jail):
            raise SystemError(u'{} should be an instance of systems.Jail'.format(jail.name))
        if jail.name in self.jails:
            raise SystemError('a jail called `{}` is already attached to `{}`'.format(jail.name, self.name))
        m = self.ip_pool
        j = jail.ip_pool
        intersec = m.intersection(j)
        if len(intersec):
            raise SystemError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        m.update(j)
        self.jail_ifconfig(jail)
        self.jails[jail.name] = jail
        jail.master = self
        return jail

    def jail_ifconfig(self, jail):
        for _if in ['ext_if', 'int_if', 'lo_if']:
            jail.__setattr__(_if, self.__getattribute__(_if))

    def clone(self, jail):
        if not isinstance(jail, Jail):
            raise SystemError(u'{} should be an instance of systems.Jail'.format(jail.name))
        _jail = copy.deepcopy(jail)
        return self.add_jail(_jail)

    @lazy
    def ezjail_admin_binary(self):
        binary = '/usr/local/bin/ezjail-admin'
        return binary


class DummyMaster(Master):
    """Describes a master that works on purely programmatic jails"""
    _ExecutorClass = DummyExecutor
