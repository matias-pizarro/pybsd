from __future__ import absolute_import, print_function, unicode_literals

import unittest

import ipaddress
import six

from pybsd.utils import safe_unicode, split_if, from_split_if


class UtilsTestCase(unittest.TestCase):

    def test_safe_unicode(self):
        if six.PY2:
            self.assertIsInstance(safe_unicode('abcd'), unicode)
            self.assertIsInstance(safe_unicode(u'abcd'), unicode)
        else:
            self.assertIsInstance(safe_unicode('abcd'), str)
            self.assertIsInstance(safe_unicode(b'abcd'), str)

    def test_split_ipv4(self):
        interface = ipaddress.ip_interface('1.2.3.4')
        self.assertListEqual(split_if(interface), [4, 32, '1', '2', '3', '4'],
                        'incorrect output')

    def test_split_ipv4_w_prefixlen(self):
        interface = ipaddress.ip_interface('1.2.3.4/24')
        self.assertListEqual(split_if(interface), [4, 24, '1', '2', '3', '4'],
                        'incorrect output')

    def test_split_ipv6(self):
        interface = ipaddress.ip_interface('a1:b2:c3:d4::')
        self.assertListEqual(split_if(interface), [6, 128, '00a1', '00b2', '00c3', '00d4', '0000', '0000', '0000', '0000'],
                        'incorrect output')

    def test_split_ipv6_w_prefixlen(self):
        interface = ipaddress.ip_interface('a1:b2:c3:d4::/110')
        self.assertListEqual(split_if(interface), [6, 110, '00a1', '00b2', '00c3', '00d4', '0000', '0000', '0000', '0000'],
                        'incorrect output')

    def test_from_split_ipv4(self):
        _list = [4, 32, '1', '2', '3', '4']
        self.assertEqual(from_split_if(_list), '1.2.3.4/32' ,
                        'incorrect output')

    def test_from_split_ipv6(self):
        _list = [6, 128, 'a1', 'b2', 'c3', 'd4', '0', '0', '0', '0']
        self.assertEqual(from_split_if(_list), 'a1:b2:c3:d4:0:0:0:0/128',
                        'incorrect output')
