# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import copy
from lazy import lazy
import logging
import re
import socket
import sys
from .commands import EzjailAdmin
from .executors import Executor, DummyExecutor
from .handlers import BaseJailHandler
from .network import Interface


__logger__ = logging.getLogger('pybsd')
IF_PROPERTY = re.compile(r'^_\w*_if$')
PATH_PROPERTY = re.compile(r'\w*(?=_path$)')


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

    def __init__(self, name, ext_if, int_if=None, lo_if=None, hostname=None):
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
    _ExecutorClass = Executor
    _JailHandlerClass = BaseJailHandler

    def __init__(self, name, ext_if, int_if=None, lo_if=None, j_if=None, jlo_if=None, hostname=None):
        super(Master, self).__init__(name, ext_if, int_if, lo_if, hostname)
        self.j_if = j_if
        self.jlo_if = jlo_if
        self.jails = {}
        self._exec = self._ExecutorClass(prefix_args=())
        self.jail_handler = self._JailHandlerClass(master=self)
        self.ezjail_admin = EzjailAdmin(master=self) # This has a method for each ezjail-admin command with parameters that mirror that of the binary

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
                raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
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
                raise EzjailError('Already attributed IPs: [{}]'.format(', '.join(intersec)))
            if _jlo_if != self.lo_if:
                self._jlo_if = _jlo_if
        else:
            self._jlo_if = None

    def add_jail(self, jail):
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
        return self.add_jail(_jail)

    @lazy
    def ezjail_admin_binary(self):
        binary = '/usr/local/bin/ezjail-admin'
        return binary

    def _ezjail_admin(self, *args):
        try:
            return self._exec(self.ezjail_admin_binary, *args)
        except socket.error:
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
        for i, cc in enumerate(lines[1]):
            if cc != '-' or i >= len(lines[0]):
                headers.append(current.strip())
                if i >= len(lines[0]):
                    break
                current = ''
            else:
                current = current + lines[0][i]
        if headers != ['STA', 'JID', 'IP', 'Hostname', 'Root Directory']:
            raise EzjailError('ezjail-admin list output has unknown headers:\n%s' % headers)
        return ('status', 'jid', 'ip', 'name', 'root')

    def __ezjail_admin(self, command, **kwargs):
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
    """Describes a master that works on purely programmatic jails"""
    _ExecutorClass = DummyExecutor

    def _exec(ezjail_admin_binary, *args):
        if args[1] == 'list':
            return (0,
                    """STA JID  IP              Hostname                       Root Directory\n"""
                    """--- ---- --------------- ------------------------------ ------------------------\n"""
                    """ZR  1    10.0.1.41/24    system             /usr/jails/system\n"""
                    """    1    re0|2a01:4f8:210:41e6::1:41:1/100\n"""
                    """    1    lo1|127.0.1.41/24\n"""
                    """    1    lo1|::1:41/100\n""",
                    '')


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
            if not isinstance(master, Master):
                raise EzjailError('{} should be an instance of systems.Master'.format(master.name))
            if name in master.jails:
                raise EzjailError('a jail called `{}` is already attached to `{}`'.format(name, master.name))
            if ids in master.ids:
                raise EzjailError('a jail with id `{}` is already attached to `{}`'.format(id, master.name))
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
            raise EzjailError('`{}` is not a valid status (it must be one of R, A or S)'.format(_status))
        self._status = _status

    @property
    def jid(self):
        return getattr(self, '_jid', None)

    @jid.setter
    def jid(self, _jid):
        """ Here we shall later hook polling of real jails if applicable"""
        if not isinstance(_jid, six.integer_types):
            raise EzjailError('`{}` is not a valid jid (it must be an integer)'.format(_jid))
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
        raise EzjailError('Jail interfaces cannot be directly set')

    @property
    def lo_if(self):
        if self.master:
            return self.master.jail_handler.get_jail_lo_if(self)
        return None

    @lo_if.setter
    def lo_if(self, _if):
        raise EzjailError('Jail interfaces cannot be directly set')
