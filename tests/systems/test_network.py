# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import unittest
from pybsd.systems.network import Interface


class InterfaceTestCase(unittest.TestCase):

    def test_no_name(self):
        with self.assertRaises(TypeError):
            Interface(ips='8.8.8.8')

    def test_name(self):
        interface = Interface(name='re0', ips='8.8.8.8')
        self.assertEqual(interface.name, 're0',
                        'incorrect name')

    def test_no_ips(self):
        with self.assertRaises(TypeError):
            Interface(name='re0')

    def test_eq_1(self):
        interface_1 = Interface(name='re0', ips=['8.8.8.8/32', '1:1:1::', '1:1:1::2/110'])
        interface_2 = Interface(name='re0', ips=['1:1:1::2/110', '1:1:1::/128', '8.8.8.8'])
        self.assertTrue(interface_1 == interface_2,
                        'incorrect name')

    def test_not_eq_prefixlen(self):
        interface_1 = Interface(name='re0', ips=['8.8.8.8/24'])
        interface_2 = Interface(name='re0', ips='8.8.8.8')
        self.assertFalse(interface_1 == interface_2,
                        'incorrect name')

    def test_not_eq_name(self):
        interface_1 = Interface(name='re0', ips='8.8.8.8')
        interface_2 = Interface(name='eth0', ips='8.8.8.8')
        self.assertFalse(interface_1 == interface_2,
                        'incorrect name')

    def test_not_eq_if4(self):
        interface_1 = Interface(name='re0', ips=['8.8.8.7', '1:1:1::', '1:1:1::2/110'])
        interface_2 = Interface(name='re0', ips=['1:1:1::2/110', '1:1:1::/128', '8.8.8.8'])
        self.assertFalse(interface_1 == interface_2,
                        'incorrect name')

    def test_not_eq_if6(self):
        interface_1 = Interface(name='re0', ips=['8.8.8.8/32', '1:1:1::', '1:1:1::1/110'])
        interface_2 = Interface(name='re0', ips=['1:1:1::2/110', '1:1:1::/128', '8.8.8.8'])
        self.assertFalse(interface_1 == interface_2,
                        'incorrect name')

    def test_ifsv4(self):
        interface = Interface(name='re0', ips='8.8.8.8/24')
        self.assertSequenceEqual(interface.ifsv4, [ipaddress.IPv4Interface('8.8.8.8/24')],
                        'incorrect ifsv4')
        self.assertSequenceEqual(interface.ifsv6, [],
                        'incorrect ifsv6')

    def test_ifsv6(self):
        interface = Interface(name='re0', ips='aa:aa:0:0::1/110')
        self.assertSequenceEqual(interface.ifsv4, [],
                        'incorrect ifsv4')
        self.assertSequenceEqual(interface.ifsv6, [ipaddress.IPv6Interface('aa:aa::1/110')],
                        'incorrect ifsv6')

    def test_ips(self):
        interface = Interface(name='re0', ips=['aa:aa:0:0::1/110', '126.6.6.8/24', 'a0:a0:0:0::1/110', '6.6.6.6/24'])
        self.assertSetEqual(interface.ips, set(['126.6.6.8', 'aa:aa::1', '6.6.6.6', 'a0:a0::1']),
                        'incorrect ips')

    def test_duplicate_ips(self):
        interface = Interface(name='re0', ips=['aa:aa:0:0::1/110', '126.6.6.8/24', 'aa:aa:0:0::1/110', '126.6.6.8/24'])
        self.assertSetEqual(interface.ips, set(['126.6.6.8', 'aa:aa::1']),
                        'incorrect ips')

    def test_ifsv24_1(self):
        interface = Interface(name='re0', ips=['aa:aa:0:0::1/110', '126.6.6.8/24', 'a0:a0:0:0::1/110', '6.6.6.6/24'])
        self.assertSequenceEqual(interface.ifsv4, [ipaddress.IPv4Interface('126.6.6.8/24'),
                            ipaddress.IPv4Interface('6.6.6.6/24')],
                        'incorrect ifsv4')
        self.assertSequenceEqual(interface.ifsv6, [ipaddress.IPv6Interface('a0:a0::1/110'),
                            ipaddress.IPv6Interface('aa:aa::1/110')],
                        'incorrect ifsv6')

    def test_ifsv24_2(self):
        interface = Interface(name='re0', ips=['aa:aa:0:0::1/110', '126.6.6.8/24', 'aa:aa:0:0::1/110', '126.6.6.8/24'])
        self.assertSequenceEqual(interface.ifsv4, [ipaddress.IPv4Interface('126.6.6.8/24')],
                        'incorrect ifsv4')
        self.assertSequenceEqual(interface.ifsv6, [ipaddress.IPv6Interface('aa:aa::1/110')],
                        'incorrect ifsv6')

    def test_main_ifv4(self):
        interface = Interface(name='re0', ips=['8.8.8.8/24', '8.8.8.1/24', '8.8.8.0/24'])
        self.assertEqual(interface.main_ifv4, ipaddress.IPv4Interface('8.8.8.0/24'),
                        'incorrect main_ifv4')

    def test_empty_ifsv4(self):
        interface = Interface(name='re0', ips=['aa:aa:0:0::1/110'])
        self.assertEqual(interface.main_ifv4, None,
                        'incorrect main_ifv4')

    def test_alias_ifsv4(self):
        interface = Interface(name='re0', ips=['8.8.8.8/24', '8.8.8.1/24', '8.8.8.0/24'])
        self.assertSequenceEqual(interface.alias_ifsv4, [ipaddress.IPv4Interface('8.8.8.1/24'),
                            ipaddress.IPv4Interface('8.8.8.8/24')],
                        'incorrect alias_ifsv4')

    def test_main_ifv6(self):
        interface = Interface(name='re0', ips=['a1:a0:0:0::1/110', 'a0:a2:0:0::1/110', 'a0:a0:0:0::1/110'])
        self.assertEqual(interface.main_ifv6, ipaddress.IPv6Interface('a0:a0::1/110'),
                        'incorrect main_ifv6')

    def test_empty_ifsv6(self):
        interface = Interface(name='re0', ips=['8.8.8.8/24', '8.8.8.1/24', '8.8.8.0/24'])
        self.assertEqual(interface.main_ifv6, None,
                        'incorrect main_ifv6')

    def test_alias_ifsv6(self):
        interface = Interface(name='re0', ips=['a1:a0:0:0::1/110', 'a0:a2:0:0::1/110', 'a0:a0:0:0::1/110'])
        self.assertSequenceEqual(interface.alias_ifsv6, [ipaddress.IPv6Interface('a0:a2:0:0::1/110'),
                            ipaddress.IPv6Interface('a1:a0:0:0::1/110')],
                        'incorrect alias_ifsv6')
