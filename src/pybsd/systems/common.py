# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import logging
from sortedcontainers import SortedListWithKey
import six
import subprocess

try:
    unicode
except NameError:  # pragma: nocover
    unicode = str


logger = logging.getLogger('pybsd')


class Interface(object):
    """Describes a network interface"""
    def __init__(self, name, ips):
        self.name = name
        self.ifsv4 = SortedListWithKey(key=lambda x: x.ip.compressed)
        self.ifsv6 = SortedListWithKey(key=lambda x: x.ip.compressed)
        self.add_ips(ips)

    def add_ips(self, ips):
        if isinstance(ips, six.string_types):
            ips = [ips]
        for ip in ips:
            _if = ipaddress.ip_interface(ip)
            if _if.ip.compressed not in self.ips:
                if _if.version == 4:
                    self.ifsv4.add(_if)
                else:
                    self.ifsv6.add(_if)

    @property
    def ips(self):
        ips = set()
        ips.update([x.ip.compressed for x in self.ifsv4])
        ips.update([x.ip.compressed for x in self.ifsv6])
        return ips

    def __eq__(self, other):
        name_eq = self.name == other.name
        ifsv4_eq = self.ifsv4 == other.ifsv4
        ifsv6_eq = self.ifsv6 == other.ifsv6
        return name_eq and ifsv4_eq and ifsv6_eq

    @property
    def main_ifv4(self):
        return self.ifsv4[0]

    @property
    def alias_ifsv4(self):
        return self.ifsv4[1:]

    @property
    def main_ifv6(self):
        return self.ifsv6[0]

    @property
    def alias_ifsv6(self):
        return self.ifsv6[1:]


class Executor:
    """Adapted from https://github.com/ployground/ploy"""
    def __init__(self, prefix_args=(), splitlines=False):
        self.prefix_args = tuple(prefix_args)
        self.splitlines = splitlines

    def __call__(self, *cmd_args, **kwargs):
        args = self.prefix_args + cmd_args
        rc = kwargs.pop('rc', None)
        out = kwargs.pop('out', None)
        err = kwargs.pop('err', None)
        stdin = kwargs.pop('stdin', None)
        logger.debug('Executing locally:\n%s', args)
        popen_kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if stdin is not None:
            popen_kwargs['stdin'] = subprocess.PIPE
        proc = subprocess.Popen(args, **popen_kwargs)
        _out, _err = proc.communicate(input=stdin)
        _rc = proc.returncode
        result = []
        if rc is None:
            result.append(_rc)
        else:
            try:
                if not any(x == _rc for x in rc):
                    raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
            except TypeError:
                pass
            if rc != _rc:
                raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
        if out is None:
            if self.splitlines:
                _out = _out.splitlines()
            result.append(_out)
        else:
            if out != _out:
                if _rc == 0:
                    logger.error(_out)
                raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
        if err is None:
            if self.splitlines:
                _err = _err.splitlines()
            result.append(_err)
        else:
            if err != _err:
                if _rc == 0:
                    logger.error(_err)
                raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
        if len(result) == 0:
            return
        elif len(result) == 1:
            return result[0]
        return tuple(result)
