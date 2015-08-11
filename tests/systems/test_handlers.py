# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import unittest
import unipath
from pybsd.systems.handlers import BaseJailHandler
from pybsd.systems.jails import Jail
from pybsd.systems.masters import Master
from pybsd.systems.network import Interface


class BaseJailHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.master = Master(name='system',
                        hostname='system.foo.bar',
                        ext_if=('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
                        int_if=('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']),
                        # lo_if=('lo0', ['127.0.0.1/24', '::1/110']),
                        j_if=('re0', ['10.0.2.0/24', '10.0.1.0/24', '1c02:4f8:0f0:14e6::2:0:1/110', '1c02:4f8:0f0:14e6::1:0:1/110']),
                        jlo_if=('lo1', ['127.0.2.0/24', '127.0.1.0/24', '::0:2:0:0/110', '::0:1:0:0/110']),)
        self.handler = self.master.jail_handler
        self.jail1 = Jail(name='jail1',
                     uid=12,
                     hostname='jail1.foo.bar',
                     master=self.master,
                     jail_type='Z',
                     auto_start=True,
                     jail_class='web',)

    def test_default_jail_root(self):
        handler = BaseJailHandler()
        self.assertEqual(handler.jail_root, unipath.Path('/usr/jails'),
                        'incorrect jail_root')

    def test_custom_jail_root(self):
        handler = BaseJailHandler(jail_root='/var/jails')
        self.assertEqual(handler.jail_root, unipath.Path('/var/jails'),
                        'incorrect jail_root')

    def test_no_master(self):
        handler = BaseJailHandler()
        self.assertEqual(handler.master, None,
                        'incorrect master')

    def test_master(self):
        self.assertEqual(self.handler.master, self.master,
                        'incorrect master')

    def test_get_jail_path(self):
        self.assertEqual(self.handler.get_jail_path(self.jail1), '/usr/jails/jail1',
                        'incorrect master')

    def test_get_jail_ext_if(self):
        ext_if = self.handler.get_jail_ext_if(self.jail1)
        self.assertIsInstance(ext_if, Interface,
                        'incorrect master')
        self.assertEqual(ext_if.name, self.master.j_if.name,
                        'incorrect master')
        self.assertNotEqual(ext_if, self.master.j_if,
                        'incorrect master')

    def test_get_jail_lo_if(self):
        lo_if = self.handler.get_jail_lo_if(self.jail1)
        self.assertIsInstance(lo_if, Interface,
                        'incorrect master')
        self.assertEqual(lo_if.name, self.master.jlo_if.name,
                        'incorrect master')
        self.assertNotEqual(lo_if, self.master.jlo_if,
                        'incorrect master')

    def test_extract_if(self):
        ext_if = self.handler.extract_if(self.master.j_if, self.jail1)
        self.assertEqual(ext_if.ifsv4, [ipaddress.IPv4Interface('10.0.2.12/24')],
                        'incorrect master')
        self.assertEqual(ext_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:f0:14e6:0:2:12:1/110')],
                        'incorrect master')

    def test_extract_if_noifv4(self):
        self.master.j_if.ifsv4.clear()
        ext_if = self.handler.extract_if(self.master.j_if, self.jail1)
        self.assertSequenceEqual(ext_if.ifsv4, [],
                        'incorrect master')

    def test_extract_if_noifv6(self):
        self.master.jlo_if.ifsv6.clear()
        lo_if = self.handler.extract_if(self.master.jlo_if, self.jail1)
        self.assertSequenceEqual(lo_if.ifsv6, [],
                        'incorrect master')
