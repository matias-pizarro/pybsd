# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import copy
from lazy import lazy
import logging
import socket
import sys
from . import System, SystemError
from .executors import Executor
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
        self.jails = {}
        if not hasattr(self, '_exec'):
            self._exec = Executor(prefix_args=())
        if not hasattr(self, 'jail_handler'):
            self.jail_handler = self._JailHandlerClass(master=self)

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

    def _ezjail_admin(self, *args):
        try:
            return self._exec(self.ezjail_admin_binary, *args)
        except socket.error:
            raise SystemError('Could not connect')

    @lazy
    def ezjail_admin_list_headers(self):
        """
        rc:  command return code
        out: command stdout
        err: command stderr
        """
        rc, out, err = self._ezjail_admin('list')
        if rc:
            raise SystemError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise SystemError('ezjail-admin list output too short:\n%s' % out.strip())
        headers = []
        current = ''
        for i, cc in enumerate(lines[1]):
            if cc != '-' or i >= len(lines[0]):
                headers.append(current.strip())
                if i >= len(lines[0]):
                    break
                current = ''
            else:
                current = current + lines[0][i]
        if headers != ['STA', 'JID', 'IP', 'Hostname', 'Root Directory']:
            raise SystemError('ezjail-admin list output has unknown headers:\n%s' % headers)
        return ('status', 'jid', 'ip', 'name', 'root')

    def ezjail_admin(self, command, **kwargs):
        # make sure there is no whitespace in the arguments
        for k, v in kwargs.items():
            if v is None:
                continue
            if command == 'console' and k == 'cmd':
                continue
            if len(v.split()) != 1:
                __logger__.error('The value `%s` of kwarg `%s` contains whitespace', v, k)
                sys.exit(1)
        if command == 'console':
            return self._ezjail_admin(
                'console',
                '-e',
                kwargs['cmd'],
                kwargs['name'])
        elif command == 'create':
            args = [
                'create',
                '-c', 'zfs']
            flavour = kwargs.get('flavour')
            if flavour is not None:
                args.extend(['-f', flavour])
            args.extend([
                kwargs['name'],
                kwargs['ip']])
            rc, out, err = self._ezjail_admin(*args)
            if rc:
                raise SystemError(err.strip())
        elif command == 'delete':
            rc, out, err = self._ezjail_admin(
                'delete',
                '-fw',
                kwargs['name'])
            if rc:
                raise SystemError(err.strip())
        elif command == 'list':
            rc, out, err = self._ezjail_admin('list')
            if rc:
                raise SystemError(err.strip())
            lines = out.splitlines()
            if len(lines) < 2:
                raise SystemError('ezjail-admin list output too short:\n%s' % out.strip())
            headers = self.ezjail_admin_list_headers
            jails = {}
            current_jail = None
            for line in lines[2:]:
                if line[0:4] != '    ':
                    line = line.strip()
                    if not line:
                        continue
                    entry = dict(zip(headers, line.split()))
                    entry['ips'] = [entry['ip']]
                    current_jail = jails[entry.pop('name')] = entry
                else:
                    line = line.strip()
                    if not line:
                        continue
                    if_ip = line.split()[1]
                    ip = if_ip.split('|')[1]
                    current_jail['ips'].append(ip)
            return jails
        elif command == 'start':
            rc, out, err = self._ezjail_admin(
                'start',
                kwargs['name'])
            if rc:
                raise SystemError(err.strip())
        elif command == 'stop':
            rc, out, err = self._ezjail_admin(
                'stop',
                kwargs['name'])
            if rc:
                raise SystemError(err.strip())
        else:
            raise ValueError('Unknown command `%s`' % command)


class DummyMaster(Master):
    """Describes a system that will host jails"""

    def _exec(self, ezjail_admin_binary, *args):
        if args[0] == 'list':
            return (0,
                    """STA JID  IP              Hostname                       Root Directory\n"""
                    """--- ---- --------------- ------------------------------ ------------------------\n"""
                    """ZR  1    10.0.1.41/24    system             /usr/jails/system\n"""
                    """    1    re0|2a01:4f8:210:41e6::1:41:1/100\n"""
                    """    1    lo1|127.0.1.41/24\n"""
                    """    1    lo1|::1:41/100\n""",
                    '')
