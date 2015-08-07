# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from lazy import lazy
import logging
import socket
import sys


__logger__ = logging.getLogger('pybsd')


class BaseCommand(object):
    """Provides a base interface to a shell command"""
    def __init__(self, env=None):
        self.env = env

    def invoke(self, *args):
        try:
            return self.env._exec(self.binary, *args)
        except socket.error:
            raise SystemError('Could not connect')

    def check_kwargs(self, subcommand, **kwargs):
        # make sure there is no whitespace in the arguments
        for k, v in kwargs.items():
            if v is None:
                continue
            if subcommand == 'console' and k == 'cmd':
                continue
            if len(v.split()) != 1:
                __logger__.error('The value `%s` of kwarg `%s` contains whitespace', v, k)
                sys.exit(1)


class EzjailAdmin(BaseCommand):
    """Provides an interface to the ezjail-admin command"""

    @property
    def binary(self):
        return self.env.ezjail_admin_binary

    @lazy
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

    @property
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
