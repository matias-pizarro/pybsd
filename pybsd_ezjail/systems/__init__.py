# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import copy
import ipaddress
from lazy import lazy
import logging
import re
import socket
import sys
import time
from .common import Interface, Executor
from .handlers import BaseJailHandler

try:
    unicode
except NameError:  # pragma: nocover
    unicode = str


log = logging.getLogger('py_ezjail')
IF_PROPERTY = re.compile(r'^_\w*_if$')
PATH_PROPERTY = re.compile(r'\w*(?=_path$)')

"""
check all system ips have an interface
jails cannot define ips. They are attributed to them by their master
through an ifconfig backend provided by systems.ipconfig. We will provide
a BaseJailHandler than can be subclassed
TBD:
    - implement check that every ip has an if
    - implement jail id
    - implement BaseIPConfigurator
    - implement systems.Master.remove_jail
    - rename systems.Master.clone clone_jail
    - organise projects
"""

class EzjailError(Exception):
    def __init__(self, *args, **kwargs):
        super(EzjailError, self).__init__(*args, **kwargs)
        if six.PY3:
            self.message = args[0]


class BaseSystem(object):
    """Describes a base OS instance, as a computer, a virtualized system or a jail"""

    def __init__(self, name, hostname=None):
        super(BaseSystem, self).__init__()
        self.name = name
        self.hostname = (hostname or name)


class System(BaseSystem):
    """Describes a full OS instance"""

    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None, **kwargs):
        super(System, self).__init__(name=name, hostname=hostname)
        self.ext_if = ext_if
        self.int_if = int_if
        self.lo_if = lo_if

    @property
    def ext_if(self):
        return self._ext_if

    @ext_if.setter
    def ext_if(self, _if):
        if_name, if_ips = _if
        _ext_if = Interface(name=if_name, ips=if_ips)
        intersec = _ext_if.ips.intersection(self.ips)
        if len(intersec):
            raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._ext_if = _ext_if

    @property
    def int_if(self):
        return self._int_if or self.ext_if

    @int_if.setter
    def int_if(self, _if):
        if _if:
            if_name, if_ips = _if
            _int_if = Interface(name=if_name, ips=if_ips)
            intersec = _int_if.ips.intersection(self.ips)
            if len(intersec):
                raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _int_if != self.ext_if:
                self._int_if = _int_if
        else:
            self._int_if = None

    @property
    def lo_if(self):
        return self._lo_if

    @lo_if.setter
    def lo_if(self, _if):
        if _if:
            if_name, if_ips = _if
        else:
            if_name = 'lo0'
            if_ips = ['127.0.0.1/8', '::1/128']
        _lo_if = Interface(name=if_name, ips=if_ips)
        intersec = _lo_if.ips.intersection(self.ips)
        if len(intersec):
            raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
        self._lo_if = _lo_if

    @property
    def ips(self):
        ips = set()
        for prop, interface in six.iteritems(self.__dict__):
            if IF_PROPERTY.match(prop) and interface:
                ips.update([x.ip.compressed for x in interface.ifsv4])
                ips.update([x.ip.compressed for x in interface.ifsv6])
        return ips


class Master(System):
    """Describes a system that will host jails"""
    _JailHandlerClass = BaseJailHandler

    def __init__(self, name, ext_if, int_if=None, lo_if=None, jlo_if=None, hostname=None, **kwargs):
        super(Master, self).__init__(name, ext_if, int_if, lo_if, hostname, **kwargs)
        self.jlo_if = jlo_if
        self.jails = {}
        if not hasattr(self, '_exec'):
            self._exec = Executor(prefix_args=())
        if not hasattr(self, '_jail_handler'):
            self._jail_handler = self._JailHandlerClass(master=self)

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
                raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _jlo_if != self.lo_if:
                self._jlo_if = _jlo_if
        else:
            self._jlo_if = None

    def _add_jail(self, jail):
        if not isinstance(jail, Jail):
            raise EzjailError(u'{} should be an instance of systems.Jail'.format(jail.name))
        if jail.name in self.jails:
            raise EzjailError('a jail called `{}` is already attached to `{}`'.format(jail.name, self.name))
        m = self.ip_pool
        j = jail.ip_pool
        intersec = m.intersection(j)
        if len(intersec):
            raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
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
            raise EzjailError(u'{} should be an instance of systems.Jail'.format(jail.name))
        _jail = copy.deepcopy(jail)
        return self._add_jail(_jail)

    @lazy
    def ezjail_admin_binary(self):
        binary = '/usr/local/bin/ezjail-admin'
        return binary

    def _ezjail_admin(self, *args):
        try:
            return self._exec(self.ezjail_admin_binary, *args)
        except socket.error as e:
            raise EzjailError('Could not connect')

    @lazy
    def ezjail_admin_list_headers(self):
        """
        rc:  command return code
        out: command stdout
        err: command stderr
        """
        rc, out, err = self._ezjail_admin('list')
        if rc:
            raise EzjailError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise EzjailError('ezjail-admin list output too short:\n%s' % out.strip())
        headers = []
        current = ''
        for i, c in enumerate(lines[1]):
            if c != '-' or i >= len(lines[0]):
                headers.append(current.strip())
                if i >= len(lines[0]):
                    break
                current = ''
            else:
                current = current + lines[0][i]
        if headers != ['STA', 'JID', 'IP', 'Hostname', 'Root Directory']:
            raise EzjailError('ezjail-admin list output has unknown headers:\n%s' % headers)
        return ('status', 'jid', 'ip', 'name', 'root')

    def ezjail_admin(self, command, **kwargs):
        # make sure there is no whitespace in the arguments
        for k, v in kwargs.items():
            if v is None:
                continue
            if command == 'console' and k == 'cmd':
                continue
            if len(v.split()) != 1:
                log.error('The value `%s` of kwarg `%s` contains whitespace', v, k)
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
                raise EzjailError(err.strip())
        elif command == 'delete':
            rc, out, err = self._ezjail_admin(
                'delete',
                '-fw',
                kwargs['name'])
            if rc:
                raise EzjailError(err.strip())
        elif command == 'list':
            rc, out, err = self._ezjail_admin('list')
            if rc:
                raise EzjailError(err.strip())
            lines = out.splitlines()
            if len(lines) < 2:
                raise EzjailError('ezjail-admin list output too short:\n%s' % out.strip())
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
                raise EzjailError(err.strip())
        elif command == 'stop':
            rc, out, err = self._ezjail_admin(
                'stop',
                kwargs['name'])
            if rc:
                raise EzjailError(err.strip())
        else:
            raise ValueError('Unknown command `%s`' % command)


class DummyMaster(Master):
    """Describes a system that will host jails"""

    def _exec(ezjail_admin_binary, *args):
        if args[1] == 'list':
            return (0,
                 'STA JID  IP              Hostname                       Root Directory\n--- ---- --------------- ------------------------------ ------------------------\nZR  1    10.0.1.41/24    agencia_tributaria             /usr/jails/agencia_tributaria\n    1    re0|2a01:4f8:210:41e6::1:41:1\n    1    lo1|127.0.1.41\n    1    lo1|::1:41\n',
                 '')


class Jail(BaseSystem):
    """Describes a jailed system"""
    master = None
    state = None
    jid = None
    allowed_main_ips = ('ext_ifv4', 'ext_ifv6', 'int_ifv4', 'int_ifv6')
    main_ip = None
    ip = None
    path = None

    def __init__(self, name, hostname=None, master=None, **kwargs):
        for _if in ['ext_if', 'int_if', 'lo_if']:
            if _if in kwargs:
                raise EzjailError('A Jail cannot define its own interfaces')
        if not isinstance(master, (Master, type(None))):
            raise EzjailError('{} should be an instance of systems.Master'.format(master.name))
        if master and name in master.jails:
            raise EzjailError('a jail called `{}` is already attached to `{}`'.format(name, master.name))
        super(Jail, self).__init__(name=name, hostname=hostname)
        # self.set_main_ip(**kwargs)
        if master:
            master._add_jail(self)

    @property
    def path(self, **kwargs):
        if self.master:
            return self.master._jail_handler.get_jail_path(self)
        return None

    """
    TBD: move to the jail handler
    """
    def set_main_ip(self, **kwargs):
        if 'main_ip' in kwargs:
            main_ip = kwargs['main_ip']
            if main_ip not in kwargs:
                raise EzjailError('Chosen main ip is not defined')
            if main_ip not in self.allowed_main_ips:
                raise EzjailError('Chosen main ip is not allowed')
        else:
            default_ip = self.allowed_main_ips[0]
            if default_ip in kwargs:
                main_ip = default_ip
            else:
                defined_ips = 0
                for main_ip in self.allowed_main_ips:
                    if main_ip in kwargs:
                        defined_ips += 1
                        if defined_ips > 1:
                            raise EzjailError('Main ip cannot be determined')
        self.ip = self.__getattribute__(main_ip)