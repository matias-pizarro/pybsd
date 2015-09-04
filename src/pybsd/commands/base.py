# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import socket

from ..exceptions import CommandConnectionError, CommandNotImplementedError, InvalidCommandExecutorError, InvalidCommandNameError

__logger__ = logging.getLogger('pybsd')


class BaseCommand(object):
    """Provides a base interface to a shell command so it can be invoked through a :py:class:`~pybsd.systems.base.BaseSystem`

    Parameters
    ----------
    env : :py:class:`~pybsd.systems.base.BaseSystem`
        The system on which the command will be will executed.

    Attributes
    ----------
    name : :py:class:`str`
        a name that identifies the command.
    binary : :py:class:`str`
        The path of the command binary on the host filesystem.

    Raises
    ------
    InvalidCommandNameError
        raised when a command doesn't have a name
    InvalidCommandExecutorError
        raised when the host system doesn't have an execyutor or it is not callable
    CommandNotImplementedError
        raised when the command's binary does not exist in the host filesystem
    CommandConnectionError
        raised when connection to a remote host fails
    """
    name = None
    binary = None

    def __init__(self, env):
        if not getattr(self, 'name', None):
            raise InvalidCommandNameError(self, env)
        if hasattr(env, 'execute') and callable(env.execute):
            self.env = env
        else:
            raise InvalidCommandExecutorError(self, env)

    def invoke(self, *args):
        """Executes the command, passing it arguments.

        Parameters
        ----------
        args : arguments that are passed to the command at execution time

        Raises
        ------
        CommandNotImplementedError
            raised when the command's binary does not exist in the host filesystem
        CommandConnectionError
            raised when connection to a remote host fails

        """
        if not getattr(self, 'binary', None):
            raise CommandNotImplementedError(self, self.env)
        try:
            return self.env.execute(self.binary, *args)
        except socket.error:
            raise CommandConnectionError(self, self.env)

    def __repr__(self):
        # Maps the command's string representation to its name
        #
        # Returns
        # -------
        # : :py:class:`str`
        #     the command's name
        return self.name
