# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from lazy import lazy
import logging
from . import CommandError
from . import BaseCommand

__logger__ = logging.getLogger('pybsd')


class EzjailAdmin(BaseCommand):
    """
    Provides an interface to the ezjail-admin command

    subcommands to be implemented:
    def __ezjail_admin(self, subcommand, **kwargs):
        # make sure there is no whitespace in the arguments
        for k, v in kwargs.items():
            if v is None:
                continue
            if subcommand == 'console' and k == 'cmd':
                continue
            if len(v.split()) != 1:
                __logger__.error('The value `%s` of kwarg `%s` contains whitespace', v, k)
                sys.exit(1)
        if subcommand == 'console':
            return self._ezjail_admin(
                'console',
                '-e',
                kwargs['cmd'],
                kwargs['name'])
        elif subcommand == 'create':
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
                raise CommandError(err.strip())
        elif subcommand == 'delete':
            rc, out, err = self._ezjail_admin(
                'delete',
                '-fw',
                kwargs['name'])
            if rc:
                raise CommandError(err.strip())
        elif subcommand == 'start':
            rc, out, err = self._ezjail_admin(
                'start',
                kwargs['name'])
            if rc:
                raise CommandError(err.strip())
        elif subcommand == 'stop':
            rc, out, err = self._ezjail_admin(
                'stop',
                kwargs['name'])
            if rc:
                raise CommandError(err.strip())
        else:
            raise ValueError('Unknown subcommand `%s`' % subcommand)
    """
    name = 'ezjail-admin'

    @property
    def binary(self):
        return self.env.ezjail_admin_binary

    def check_kwargs(self, subcommand, **kwargs):
        # make sure there is no whitespace in the arguments
        for k, v in kwargs.items():
            if v is None:
                continue
            if subcommand == 'console' and k == 'cmd':
                continue
            if len(v.split()) != 1:
                raise CommandError('The value `{}` of kwarg `{}` contains whitespace'.format(v, k))

    @lazy
    def list_headers(self):
        """
        rc:  command return code
        out: command stdout
        err: command stderr
        """
        rc, out, err = self.invoke('list')
        if rc:
            raise CommandError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise CommandError('ezjail-admin list output too short:\n%s' % out.strip())
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
            raise CommandError('ezjail-admin list output has unknown headers:\n%s' % headers)
        return ('status', 'jid', 'ip', 'name', 'root')

    @property
    def list(self):
        rc, out, err = self.invoke('list')
        if rc:
            raise CommandError(err.strip())
        lines = out.splitlines()
        if len(lines) < 2:
            raise CommandError('ezjail-admin list output too short:\n%s' % out.strip())
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
