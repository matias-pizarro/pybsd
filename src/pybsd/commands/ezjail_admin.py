# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import lazy
import logging
from . import BaseCommand

__logger__ = logging.getLogger('pybsd')


class EzjailAdmin(BaseCommand):
    """Provides an interface to the ezjail-admin command"""

    name = 'ezjail-admin'

    @property
    def binary(self):
        return self.env.ezjail_admin_binary

    @classmethod
    def check_kwargs(cls, subcommand, **kwargs):
        # make sure there is no whitespace in the arguments
        for key, value in kwargs.items():
            if value is None:
                continue
            if subcommand == 'console' and key == 'cmd':
                continue
            if len(value.split()) != 1:
                raise SystemError('The value `{}` of kwarg `{}` contains whitespace'.format(value, key))

    @lazy.lazy
    def list_headers(self):
        """
        rc:  command return code
        out: command stdout
        err: command stderr
        """
        rc, out, err = self.invoke('list')
        if rc:
            raise SystemError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise SystemError('ezjail-admin list output too short:\n%s' % out.strip())
        headers = []
        current = ''
        for pos, char in enumerate(lines[1]):
            if char != '-' or pos >= len(lines[0]):
                headers.append(current.strip())
                if pos >= len(lines[0]):
                    break
                current = ''
            else:
                current = current + lines[0][pos]
        if headers != ['STA', 'JID', 'IP', 'Hostname', 'Root Directory']:
            raise SystemError('ezjail-admin list output has unknown headers:\n%s' % headers)
        return ('status', 'jid', 'ip', 'name', 'root')

    def list(self):
        rc, out, err = self.invoke('list')
        if rc:
            raise SystemError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise SystemError('ezjail-admin list output too short:\n%s' % out.strip())
        headers = self.list_headers
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

    def console(self, cmd, jail_name):
        self.check_kwargs('console', cmd=cmd, jail_name=jail_name)
        rc, out, err = self.invoke('console',
                                   '-e',
                                   cmd,
                                   jail_name)
        return out

    # subcommands to be implemented:
    # def __ezjail_admin(self, subcommand, **kwargs):
    #     # make sure there is no whitespace in the arguments
    #     for key, value in kwargs.items():
    #         if value is None:
    #             continue
    #         if subcommand == 'console' and key == 'cmd':
    #             continue
    #         if len(value.split()) != 1:
    #             __logger__.error('The value `%s` of kwarg `%s` contains whitespace', value, key)
    #             sys.exit(1)
    #     if subcommand == 'console':
    #         return self._ezjail_admin(
    #             'console',
    #             '-e',
    #             kwargs['cmd'],
    #             kwargs['name'])
    #     elif subcommand == 'create':
    #         args = [
    #             'create',
    #             '-c', 'zfs']
    #         flavour = kwargs.get('flavour')
    #         if flavour is not None:
    #             args.extend(['-f', flavour])
    #         args.extend([
    #             kwargs['name'],
    #             kwargs['ip']])
    #         rc, out, err = self._ezjail_admin(*args)
    #         if rc:
    #             raise SystemError(err.strip())
    #     elif subcommand == 'delete':
    #         rc, out, err = self._ezjail_admin(
    #             'delete',
    #             '-fw',
    #             kwargs['name'])
    #         if rc:
    #             raise SystemError(err.strip())
    #     elif subcommand == 'start':
    #         rc, out, err = self._ezjail_admin(
    #             'start',
    #             kwargs['name'])
    #         if rc:
    #             raise SystemError(err.strip())
    #     elif subcommand == 'stop':
    #         rc, out, err = self._ezjail_admin(
    #             'stop',
    #             kwargs['name'])
    #         if rc:
    #             raise SystemError(err.strip())
    #     else:
    #         raise ValueError('Unknown subcommand `%s`' % subcommand)
