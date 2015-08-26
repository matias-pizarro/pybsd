# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
import socket
from ..exceptions import InvalidCommandNameError, InvalidCommandExecutorError, CommandNotImplementedError, CommandConnectionError

__logger__ = logging.getLogger('pybsd')


class BaseCommand(object):
    """Provides a base interface to a shell command"""
    name = None

    def __init__(self, env):
        if not getattr(self, 'name', None):
            raise InvalidCommandNameError(self, env)
        if hasattr(env, 'execute') and callable(env.execute):
            self.env = env
        else:
            raise InvalidCommandExecutorError(self, env)

    def invoke(self, *args):
        if not getattr(self, 'binary', None):
            raise CommandNotImplementedError(self, self.env)
        try:
            return self.env.execute(self.binary, *args)
        except socket.error:
            raise CommandConnectionError(self, self.env)

    def __repr__(self):
        # Maps the command's string representation to its name
        return self.name
