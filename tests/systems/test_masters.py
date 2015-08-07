# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
from pybsd.systems import EzjailError
from pybsd.systems.masters import Master, DummyMaster
from pybsd.systems.handlers import BaseJailHandler
from .test_systems import SystemTestCase


class MasterTestCase(SystemTestCase):

    system_class = Master
    params = {
        'name': 'system',
        'hostname': 'system.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24']),
        'j_if': ('re0', ['10.0.0.0/24']),
        'jlo_if': ('lo1', ['127.0.1.0/24']),
    }

    def test_j_if_name(self):
        self.assertEqual(self.system.j_if.name, 're0',
                        'incorrect j_if name')

    def test_j_if_ifsv4(self):
        self.assertSequenceEqual(self.system.j_if.ifsv4, [ipaddress.IPv4Interface('10.0.0.0/24')],
                        'incorrect j_if ifsv4')
        self.assertSequenceEqual(self.system.j_if.ifsv6, [],
                        'incorrect j_if ifsv6')

    def test_j_if_ifsv6(self):
        j_if = ('re0', ['1:1:1::2/110'])
        self.system.j_if = j_if
        self.assertSequenceEqual(self.system.j_if.name, 're0',
                        'incorrect j_if name')
        self.assertSequenceEqual(self.system.j_if.ifsv4, [],
                        'incorrect j_if ifsv4')
        self.assertSequenceEqual(self.system.j_if.ifsv6, [ipaddress.IPv6Interface('1:1:1::2/110')],
                        'incorrect j_if ifsv6')

    def test_no_j_if_name(self):
        params = self.params.copy()
        del params['j_if']
        system = self.system_class(**params)
        self.assertEqual(system.j_if.name, 're0',
                        'incorrect j_if name')

    def test_no_j_if_ifsv4(self):
        params = self.params.copy()
        del params['j_if']
        system = self.system_class(**params)
        self.assertSequenceEqual(system.j_if.ifsv4, [ipaddress.IPv4Interface('8.8.8.8/24')],
                        'incorrect j_if ifsv4')
        self.assertSequenceEqual(system.j_if.ifsv6, [],
                        'incorrect j_if ifsv6')

    def test_duplicate_j_if(self):
        params = self.params.copy()
        params['j_if'] = ('re0', ['8.8.8.8/24'])
        with self.assertRaises(EzjailError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message, u'Already attributed IPs: [8.8.8.8]')

    def test_jlo_if_name(self):
        self.assertEqual(self.system.jlo_if.name, 'lo1',
                        'incorrect jlo_if name')

    def test_jlo_if_ifsv4(self):
        self.assertSequenceEqual(self.system.jlo_if.ifsv4, [ipaddress.IPv4Interface('127.0.1.0/24')],
                        'incorrect jlo_if ifsv4')
        self.assertSequenceEqual(self.system.jlo_if.ifsv6, [],
                        'incorrect jlo_if ifsv6')

    def test_jlo_if_ifsv6(self):
        jlo_if = ('re0', ['1:1:1::2/110'])
        self.system.jlo_if = jlo_if
        self.assertSequenceEqual(self.system.jlo_if.name, 're0',
                        'incorrect jlo_if name')
        self.assertSequenceEqual(self.system.jlo_if.ifsv4, [],
                        'incorrect jlo_if ifsv4')
        self.assertSequenceEqual(self.system.jlo_if.ifsv6, [ipaddress.IPv6Interface('1:1:1::2/110')],
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
        params['jlo_if'] = ('lo1', ['127.0.0.1/24'])
        with self.assertRaises(EzjailError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message, u'Already attributed IPs: [127.0.0.1]')

    def test_jail_handler(self):
        self.assertIsInstance(self.system.jail_handler, BaseJailHandler,
                        'incorrect jail_handler')
        self.assertEqual(self.system.jail_handler.master, self.system,
                        'incorrect jail_handler')

    def test_dummy_master__exec(self):
        system = DummyMaster(**self.params)
        self.assertSequenceEqual(system.ezjail_admin('list'),
                                {u'system': {u'status': u'ZR',
                                                         u'jid': u'1',
                                                         u'ip': u'10.0.1.41/24',
                                                         u'ips': [u'10.0.1.41/24',
                                                                  u'2a01:4f8:210:41e6::1:41:1/100',
                                                                  u'127.0.1.41/24',
                                                                  u'::1:41/100'],
                                                         u'root': u'/usr/jails/system'
                                      }
                                },
                        'incorrect ezjail-admin list output')
