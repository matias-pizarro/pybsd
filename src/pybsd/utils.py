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


def split_if(interface):
    """Returns a list-based description of an :py:class:`ipaddress.IPVxInterface`'s ip and prefixlen

    Some significative indexes of the list always describe the same aspect of the interface:
        * 0: version
        * 1: prefixlen
        * 2: first octet of the interface's ip address
        * -1: last octet of the interface's ip address

    Parameters
    ----------
    interface : :py:class:`ipaddress.IPV4Interface` or :py:class:`ipaddress.IPV6Interface`
        the interface to be described

    Returns
    -------
    : :py:class:`list`
        a list of 6 (IPv4) or 10 (IPv6) elements describing an interface
    """
    sep = '.' if interface.version == 4 else ':'
    chunks = interface.ip.exploded.split(sep)
    chunks.insert(0, interface.version)
    chunks.insert(1, interface.network.prefixlen)
    return chunks


def from_split_if(chunks):
    """Converts a list-based description of an :py:class:`ipaddress.IPVxInterface`'s ip and prefixlen such as that returned
    by :py:meth:`pybsd.utils.split_if` into a string.

    The returned string can be used as the argument to :py:meth:`ipaddress.ip_interface`

    Parameters
    ----------
    chunks: :py:class:`list`
        a list of 6 (IPv4) or 10 (IPv6) elements describing an interface

    Returns
    -------
    : :py:class:`str`
        a string-based description of an :py:class:`ipaddress.IPVxInterface`'s ip and prefixlen
    """
    version = chunks.pop(0)
    prefixlen = chunks.pop(0)
    sep = '.' if version == 4 else ':'
    return '{}/{}'.format(sep.join(chunks), str(prefixlen))
