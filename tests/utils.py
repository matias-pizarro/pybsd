# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six

def extract_message(context_manager):
    return  context_manager.exception.message if six.PY2 else context_manager.exception.args[0]
