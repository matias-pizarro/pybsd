# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import six

__logger__ = logging.getLogger('pybsd')


def safe_unicode(string):
    """Converts a string to unicode

    Parameters
    ----------
    string : :py:class:`basestring` (python 2/3) or :py:class:`str` (python 2/3) or :py:class:`unicode` (python 2) \
    or :py:class:`bytes` (python 3)
        the string to be converted

    Returns
    -------
    : :py:class:`unicode` (python 2) or :py:class:`str` (python 3)
        a unicode string

    """
    if isinstance(string, six.binary_type):
        string = string.decode('utf8')
    return string
