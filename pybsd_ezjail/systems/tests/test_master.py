# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import six
from .. import Master, EzjailError
from .test_system import SystemTestCase


class MasterTestCase(SystemTestCase):

    system_class = Master
    params = {
        'name': 'system',
        'hostname': 'system.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24']),
        'jlo_if': ('lo1', ['127.0.1.0/24'])
    }

    def test_jlo_if_name(self):
        self.assertEqual(self.system.jlo_if.name, 'lo1',
                        'incorrect jlo_if name')

    def test_jlo_if_ifsv4(self):
        self.assertSequenceEqual(self.system.jlo_if.ifsv4, [ipaddress.IPv4Interface('127.0.1.0/24')],
                        'incorrect jlo_if ifsv4')
        self.assertSequenceEqual(self.system.jlo_if.ifsv6, [],
                        'incorrect jlo_if ifsv6')

    def test_no_jlo_if_name(self):
        params = self.params.copy()
        del params['jlo_if']
        system = self.system_class(**params)
        self.assertEqual(system.jlo_if.name, 'lo0',
                        'incorrect jlo_if name')

    def test_no_jlo_if_ifsv4(self):
        params = self.params.copy()
        del params['jlo_if']
        system = self.system_class(**params)
        self.assertSequenceEqual(system.jlo_if.ifsv4, [ipaddress.IPv4Interface('127.0.0.1/8')],
                        'incorrect jlo_if ifsv4')
        self.assertSequenceEqual(system.jlo_if.ifsv6, [ipaddress.IPv6Interface('::1/128')],
                        'incorrect jlo_if ifsv6')

    def test_duplicate_jlo_if(self):
        params = self.params.copy()
        params['jlo_if'] = ('lo0', ['127.0.0.1/24'])
        with self.assertRaises(EzjailError) as cm:
            system = self.system_class(**params)
        self.assertEqual(cm.exception.message, u'Already attributed IPs: [127.0.0.1]')
