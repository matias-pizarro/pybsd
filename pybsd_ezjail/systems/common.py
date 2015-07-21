# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
import subprocess

try:
    unicode
except NameError:  # pragma: nocover
    unicode = str


log = logging.getLogger('py_ezjail')


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
        log.debug('Executing locally:\n%s', args)
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
                    log.error(_out)
                raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
        if err is None:
            if self.splitlines:
                _err = _err.splitlines()
            result.append(_err)
        else:
            if err != _err:
                if _rc == 0:
                    log.error(_err)
                raise subprocess.CalledProcessError(_rc, ' '.join(args), _err)
        if len(result) == 0:
            return
        elif len(result) == 1:
            return result[0]
        return tuple(result)
