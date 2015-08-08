# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
import socket
from ...exceptions import SystemError

__logger__ = logging.getLogger('pybsd')


class CommandError(SystemError):
    pass


class BaseCommand(object):
    """Provides a base interface to a shell command"""
    name = None

    def __init__(self, env):
        if not getattr(self, 'name', None):
            raise CommandError('`name` property is missing')
        if hasattr(env, '_exec') and callable(env._exec):
            self.env = env
        else:
            raise SystemError('`{}` must have a callable Executor method'.format(env))

    def invoke(self, *args):
        if not getattr(self, 'binary', None):
            raise NotImplementedError('`{}` is not implemented on this system'.format(self.name))
        try:
            return self.env._exec(self.binary, *args)
        except socket.error:
            raise SystemError('Could not connect')
