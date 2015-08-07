# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
from pybsd.systems import System, SystemError
from .test_base_system import BaseSystemTestCase


class SystemTestCase(BaseSystemTestCase):

    system_class = System
    params = {
        'name': 'system',
        'hostname': 'system.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24'])
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
        self.assertSequenceEqual(self.system.ext_if.ifsv4, [ipaddress.IPv4Interface('8.8.8.8/24')],
                        'incorrect ext_if ifsv4')
        self.assertSequenceEqual(self.system.ext_if.ifsv6, [],
                        'incorrect ext_if ifsv6')

    def test_ext_if_ifsv6(self):
        ext_if = ('re0', ['1:1:1::2/110'])
        self.system.ext_if = ext_if
        self.assertSequenceEqual(self.system.ext_if.name, 're0',
                        'incorrect ext_if name')
        self.assertSequenceEqual(self.system.ext_if.ifsv4, [],
                        'incorrect ext_if ifsv4')
        self.assertSequenceEqual(self.system.ext_if.ifsv6, [ipaddress.IPv6Interface('1:1:1::2/110')],
                        'incorrect ext_if ifsv6')

    def test_duplicate_ext_if(self):
        with self.assertRaises(SystemError) as context_manager:
            self.system.ext_if = ('re0', ['192.168.0.0/24'])
        self.assertEqual(context_manager.exception.message, u'Already attributed IPs: [192.168.0.0]')

    def test_int_if_name(self):
        self.assertEqual(self.system.int_if.name, 'eth0',
                        'incorrect int_if name')

    def test_int_if_ifsv4(self):
        self.assertSequenceEqual(self.system.int_if.ifsv4, [ipaddress.IPv4Interface('192.168.0.0/24')],
                        'incorrect int_if ifsv4')
        self.assertSequenceEqual(self.system.int_if.ifsv6, [],
                        'incorrect int_if ifsv6')

    def test_int_if_ifsv6(self):
        int_if = ('re0', ['1:1:1::2/110'])
        self.system.int_if = int_if
        self.assertSequenceEqual(self.system.int_if.name, 're0',
                        'incorrect int_if name')
        self.assertSequenceEqual(self.system.int_if.ifsv4, [],
                        'incorrect int_if ifsv4')
        self.assertSequenceEqual(self.system.int_if.ifsv6, [ipaddress.IPv6Interface('1:1:1::2/110')],
                        'incorrect int_if ifsv6')

    def test_no_int_if_name(self):
        params = self.params.copy()
        del params['int_if']
        system = self.system_class(**params)
        self.assertEqual(system.int_if.name, 're0',
                        'incorrect int_if name')

    def test_no_int_if_ifsv4(self):
        params = self.params.copy()
        del params['int_if']
        system = self.system_class(**params)
        self.assertSequenceEqual(system.int_if.ifsv4, [ipaddress.IPv4Interface('8.8.8.8/24')],
                        'incorrect int_if ifsv4')
        self.assertSequenceEqual(system.int_if.ifsv6, [],
                        'incorrect int_if ifsv6')

    def test_duplicate_int_if(self):
        params = self.params.copy()
        params['int_if'] = ('eth0', ['8.8.8.8/24'])
        with self.assertRaises(SystemError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message, u'Already attributed IPs: [8.8.8.8]')

    def test_no_lo_if_name(self):
        self.assertEqual(self.system.lo_if.name, 'lo0',
                        'incorrect lo_if name')

    def test_no_lo_if(self):
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.0.1/8')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [ipaddress.IPv6Interface('::1/128')],
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
        params['lo_if'] = ('lo0', ['8.8.8.8/24'])
        with self.assertRaises(SystemError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message, u'Already attributed IPs: [8.8.8.8]')

    def test_lo_if_ifsv4(self):
        lo_if = ('lo1', ['127.0.0.2/8'])
        self.system.lo_if = lo_if
        self.assertSequenceEqual(self.system.lo_if.name, 'lo1',
                        'incorrect lo_if name')
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.0.2/8')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [],
                        'incorrect lo_if ifsv6')

    def test_lo_if_ifsv6(self):
        lo_if = ('re0', ['1:1:1::2/110'])
        self.system.lo_if = lo_if
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [ipaddress.IPv6Interface('1:1:1::2/110')],
                        'incorrect lo_if ifsv6')
