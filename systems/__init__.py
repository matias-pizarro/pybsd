# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import copy
import ipaddr
from lazy import lazy
import logging
import re
import socket
import sys
import time
import unipath
from .common import Executor


log = logging.getLogger('py_ezjail')
IP_PROPERTY = re.compile(r'\w*_ipv(4|6)$')
PATH_PROPERTY = re.compile(r'\w*(?=_path$)')


class EzjailError(Exception):
    pass


class System(object):
    """Describes an OS instance, as a computer, a virtualized system or a jail"""
    name = None
    hostname = None
    ext_if = None
    int_if = None
    lo_if = None
    ip_pool = None
    ext_ipv4 = None
    ext_ipv6 = None
    int_ipv4 = None
    int_ipv6 = None
    lo_ipv4 = None
    lo_ipv6 = None

    def __init__(self, name, **kwargs):
        super(System, self).__init__()
        self.name = name
        self.ip_pool = set()
        self._set_properties(kwargs, ['hostname', 'ext_if', 'int_if', 'lo_if', 'ext_ipv4',
            'ext_ipv6', 'int_ipv4', 'int_ipv6', 'lo_ipv4', 'lo_ipv6'])

    def ip_pool_check(self, ip):
        if ip in self.ip_pool:
            raise EzjailError('IP address {} has already been attributed'.format(ip))
        self.ip_pool.add(ip)
        return True

    def _set_properties(self, kwargs, kws):
        for kw in kws:
            val = kwargs[kw] if kw in kwargs else self.__getattribute__(kw)
            if val:
                if IP_PROPERTY.match(kw):
                    val = ipaddr.IPNetwork(val)
                    self.ip_pool_check(val.ip.compressed)
                path = PATH_PROPERTY.match(kw)
                if path:
                    kw = path.group()
                    val = unipath.Path(val)
                # print(kw, val)
                self.__setattr__(kw, val)


class Master(System):
    """Describes a system that will host jails"""
    _exec = None
    jlo_if = None
    jail_root_path = '/usr/jails'
    jails = None

    def __init__(self, name, **kwargs):
        super(Master, self).__init__(name, **kwargs)
        prefix_args = ()
        if self._exec is None:
            self._exec = Executor(prefix_args=prefix_args)
        self.jails = {}
        self._set_properties(kwargs, ['jlo_if', 'jail_root_path'])

    def add_jail(self, _jail, _new=False):
        if not isinstance(_jail, Jail):
            raise EzjailError(u'{} should be an instance of systems.Jail'.format(_jail.name))
        jail = _jail if _new else copy.deepcopy(_jail)
        if jail.name not in self.jails:
            m = self.ip_pool
            j = jail.ip_pool
            intersec = m.intersection(j)
            if len(intersec):
                raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            m.update(j)
            for _if in ['ext_if', 'int_if', 'lo_if']:
                jail.__setattr__(_if, self.__getattribute__(_if))
            jail.path = self.jail_root.child(jail.name)
            self.jails[jail.name] = jail
            jail.master = self

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
                log.error("The value '%s' of kwarg '%s' contains whitespace", v, k)
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
            raise ValueError("Unknown command '%s'" % command)


class DummyMaster(Master):
    """Describes a system that will host jails"""

    def _exec(ezjail_admin_binary, *args):
        if args[1] == 'list':
            return (0,
                 'STA JID  IP              Hostname                       Root Directory\n--- ---- --------------- ------------------------------ ------------------------\nZR  1    10.0.1.41/24    agencia_tributaria             /usr/jails/agencia_tributaria\n    1    re0|2a01:4f8:210:41e6::1:41:1\n    1    lo1|127.0.1.41\n    1    lo1|::1:41\n',
                 '')


class Jail(System):
    """Describes a jailed system"""
    master = None
    state = None
    jid = None
    allowed_main_ips = ('ext_ipv4', 'ext_ipv6', 'int_ipv4', 'int_ipv6')
    main_ip = None
    ip = None
    path = None

    def __new__(cls, *args, **kwargs):
        if 'master' in kwargs:
            master = kwargs['master']
            if not isinstance(master, Master):
                raise EzjailError('{} should be an instance of systems.Master'.format(master.name))
            if len(args):
                name = args[0]
                if name in master.jails:
                    return master.jails[name]
        return super(Jail, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name, master=None, **kwargs):
        for _if in ['ext_if', 'int_if', 'lo_if']:
            if _if in kwargs:
                raise EzjailError('A Jail cannot define its own interfaces')
        super(Jail, self).__init__(name, **kwargs)
        self.set_main_ip(**kwargs)
        if master:
            master.add_jail(self, _new=True)
        else:
            self.path = unipath.Path('foo', name)

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