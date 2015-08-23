# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
from pybsd import System
from .. import extract_message
from .test_base_system import BaseSystemTestCase


class SystemTestCase(BaseSystemTestCase):

    system_class = System
    params = {
        'name': 'system',
        'hostname': 'system.foo.bar',
        'ext_if': ('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
        'int_if': ('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']),
    }

    def test_no_ext_if(self):
        params = self.params.copy()
        del params['ext_if']
        with self.assertRaises(TypeError):
            self.system = self.system_class(**params)

    def test_ext_if_name(self):
        self.assertEqual(self.system.ext_if.name, 're0',
                        'incorrect ext_if name')

    def test_ext_if_ifsv4(self):
        self.assertSequenceEqual(self.system.ext_if.ifsv4, [ipaddress.IPv4Interface('148.241.178.106/24')],
                        'incorrect ext_if ifsv4')

    def test_ext_if_ifsv6(self):
        self.assertSequenceEqual(self.system.ext_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::/110')],
                        'incorrect ext_if ifsv6')

    def test_duplicate_ext_if(self):
        params = self.params.copy()
        params['ext_if'] = ('eth0', ['192.168.0.0/24'])
        with self.assertRaises(SystemError) as context_manager:
            self.system_class(**params)
        self.assertEqual(extract_message(context_manager), u'Already attributed IPs: [192.168.0.0]')

    def test_int_if_name(self):
        self.assertEqual(self.system.int_if.name, 'eth0',
                        'incorrect int_if name')

    def test_int_if_ifsv4(self):
        self.assertSequenceEqual(self.system.int_if.ifsv4, [ipaddress.IPv4Interface('192.168.0.0/24')],
                        'incorrect int_if ifsv4')

    def test_int_if_ifsv6(self):
        self.assertSequenceEqual(self.system.int_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::0:0:1/110')],
                        'incorrect int_if ifsv6')

    def test_no_int_if_name(self):
        params = self.params.copy()
        del params['int_if']
        system = self.system_class(**params)
        self.assertEqual(system.int_if.name, 're0',
                        'incorrect int_if name')

    def test_no_int_if_ifs(self):
        params = self.params.copy()
        del params['int_if']
        system = self.system_class(**params)
        self.assertSequenceEqual(system.int_if.ifsv4, [ipaddress.IPv4Interface('148.241.178.106/24')],
                        'incorrect int_if ifsv4')
        self.assertSequenceEqual(self.system.int_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::0:0:1/110')],
                        'incorrect ext_if ifsv6')

    def test_duplicate_int_if(self):
        params = self.params.copy()
        params['int_if'] = ('eth0', ['148.241.178.106/24'])
        with self.assertRaises(SystemError) as context_manager:
            self.system_class(**params)
        self.assertEqual(extract_message(context_manager), u'Already attributed IPs: [148.241.178.106]')

    def test_no_lo_if_name(self):
        self.assertEqual(self.system.lo_if.name, 'lo0',
                        'incorrect lo_if name')

    def test_no_lo_if(self):
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.0.1/8')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [ipaddress.IPv6Interface('::1/110')],
                        'incorrect lo_if ifsv6')

    def test_lo_if_name(self):
        params = self.params.copy()
        params['lo_if'] = ('lo1', '10.0.0.1/8')
        system = self.system_class(**params)
        self.assertEqual(system.lo_if.name, 'lo1',
                        'incorrect lo_if name')

    def test_lo_if(self):
        params = self.params.copy()
        params['lo_if'] = ('lo1', ['10.0.0.1/8', '1:1::/128'])
        system = self.system_class(**params)
        self.assertSequenceEqual(system.lo_if.ifsv4, [ipaddress.IPv4Interface('10.0.0.1/8')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(system.lo_if.ifsv6, [ipaddress.IPv6Interface('1:1::/128')],
                        'incorrect lo_if ifsv6')

    def test_duplicate_lo_if(self):
        params = self.params.copy()
        params['lo_if'] = ('lo0', ['148.241.178.106/24'])
        with self.assertRaises(SystemError) as context_manager:
            self.system_class(**params)
        self.assertEqual(extract_message(context_manager), u'Already attributed IPs: [148.241.178.106]')

    def test_lo_if_ifsv4(self):
        params = self.params.copy()
        params['lo_if'] = ('lo1', ['127.0.0.2/8'])
        self.system = self.system_class(**params)
        self.assertSequenceEqual(self.system.lo_if.name, 'lo1',
                        'incorrect lo_if name')
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.0.2/8')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [],
                        'incorrect lo_if ifsv6')

    def test_lo_if_ifsv6(self):
        params = self.params.copy()
        params['lo_if'] = ('re0', ['::2/110'])
        self.system = self.system_class(**params)
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [ipaddress.IPv6Interface('::2/110')],
                        'incorrect lo_if ifsv6')

    def test_reset_int_if(self):
        self.system.reset_int_if()
        self.assertEqual(self.system.int_if, self.system.ext_if,
                        'systems.master.Master.reset_int_if is broken')
