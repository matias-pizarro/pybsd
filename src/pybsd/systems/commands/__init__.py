# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
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
