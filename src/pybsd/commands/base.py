# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
import socket
from ..exceptions import InvalidCommandName

__logger__ = logging.getLogger('pybsd')


class BaseCommand(object):
    """Provides a base interface to a shell command"""
    name = None

    def __init__(self, env):
        if not getattr(self, 'name', None):
            raise InvalidCommandName(self)
        if hasattr(env, 'execute') and callable(env.execute):
            self.env = env
        else:
            raise SystemError('`{}` must have a callable Executor method'.format(env))

    def invoke(self, *args):
        if not getattr(self, 'binary', None):
            raise NotImplementedError('`{}` is not implemented on this system'.format(self.name))
        try:
            return self.env.execute(self.binary, *args)
        except socket.error:
            raise SystemError('Could not connect')

    def __repr__(self):
        # Maps the command's string representation to its name
        return self.name
