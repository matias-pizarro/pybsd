# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import logging

__logger__ = logging.getLogger('pybsd')


class SystemError(Exception):
    def __init__(self, *args, **kwargs):
        super(SystemError, self).__init__(*args, **kwargs)
        if six.PY3:
            self.message = args[0]
