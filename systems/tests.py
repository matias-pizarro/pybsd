# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddr
import unipath
import unittest
from . import System, Master, DummyMaster, Jail, EzjailError


class SystemTestCase(unittest.TestCase):
    """
    Somewhere down the line, the bleeding obvious comes back to kick our ass
    My bleeding obvious might not be your bleeding obvious
    Somewhere down the line the bleeding obvious might not seem so obvious
    Tests are part of the documentation
    Redundancy in tests is a feature, not an issue
    """
    system_class = System

    def test_name(self):
        system = self.system_class('system')
        self.assertEqual(system.name, 'system',
                        'incorrect name')

    def test_empty_ip_pool(self):
        system = self.system_class('system')
        self.assertEqual(system.ip_pool, set(),
                        'incorrect ip_pool')

    def test_ip_pool(self):
        system = self.system_class('system', ext_ipv4='8.8.8.8/24')
        self.assertSetEqual(system.ip_pool, set(['8.8.8.8']),
                        'incorrect ip_pool')

    def test_ip_pool_2(self):
        system = self.system_class('system', ext_ipv4='8.8.8.8/24',
            int_ipv4='8.8.8.9/24')
        self.assertSetEqual(system.ip_pool, set(['8.8.8.8', '8.8.8.9']),
                        'incorrect ip_pool')

    def test_duplicate_ip(self):
        with self.assertRaises(EzjailError) as cm:
            system = self.system_class('system', ext_ipv4='8.8.8.8/24',
                int_ipv4='8.8.8.8/24')
        self.assertEqual(cm.exception.message, u'IP address 8.8.8.8 has already been attributed')

    def test_hostname(self):
        system = self.system_class('system', hostname='system.foo.bar')
        self.assertEqual(system.hostname, 'system.foo.bar',
                        'incorrect hostname')

    def test_ext_if(self):
        system = self.system_class('system', ext_if='re0')
        self.assertEqual(system.ext_if, 're0',
                        'incorrect ext_if')

    def test_int_if(self):
        system = self.system_class('system', int_if='ath0')
        self.assertEqual(system.int_if, 'ath0',
                        'incorrect int_if')

    def test_lo_if(self):
        system = self.system_class('system', lo_if='lo0')
        self.assertEqual(system.lo_if, 'lo0',
                        'incorrect lo_if')

    def test_ext_ipv4(self):
        system = self.system_class('system', ext_ipv4='8.8.8.8')
        self.assertIsInstance(system.ext_ipv4, ipaddr.IPv4Network,
                        'incorrect ext_ipv4')
        self.assertIsInstance(system.ext_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv4.prefixlen, 32,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect ext_ipv4')

    def test_ext_ipv4_masked(self):
        system = self.system_class('system', ext_ipv4='8.8.8.8/24')
        self.assertIsInstance(system.ext_ipv4, ipaddr.IPv4Network,
                        'incorrect ext_ipv4')
        self.assertIsInstance(system.ext_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv4.prefixlen, 24,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect ext_ipv4')

    def test_ext_ipv6(self):
        system = self.system_class('system', ext_ipv6='2a:2a::2a')
        self.assertIsInstance(system.ext_ipv6, ipaddr.IPv6Network,
                        'incorrect ext_ipv6')
        self.assertIsInstance(system.ext_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect ext_ipv6')
        self.assertEqual(system.ext_ipv6.prefixlen, 128,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv6.ip.compressed, '2a:2a::2a',
                        'incorrect ext_ipv6')

    def test_ext_ipv6_masked(self):
        system = self.system_class('system', ext_ipv6='2a:2a::2a/100')
        self.assertIsInstance(system.ext_ipv6, ipaddr.IPv6Network,
                        'incorrect ext_ipv6')
        self.assertIsInstance(system.ext_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect ext_ipv6')
        self.assertEqual(system.ext_ipv6.prefixlen, 100,
                        'incorrect ext_ipv4')
        self.assertEqual(system.ext_ipv6.ip.compressed, '2a:2a::2a',
                        'incorrect ext_ipv6')

    def test_int_ipv4(self):
        system = self.system_class('system', int_ipv4='8.8.8.8')
        self.assertIsInstance(system.int_ipv4, ipaddr.IPv4Network,
                        'incorrect int_ipv4')
        self.assertIsInstance(system.int_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv4.prefixlen, 32,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect int_ipv4')

    def test_int_ipv4_masked(self):
        system = self.system_class('system', int_ipv4='8.8.8.8/24')
        self.assertIsInstance(system.int_ipv4, ipaddr.IPv4Network,
                        'incorrect int_ipv4')
        self.assertIsInstance(system.int_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv4.prefixlen, 24,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect int_ipv4')

    def test_int_ipv6(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a')
        self.assertIsInstance(system.int_ipv6, ipaddr.IPv6Network,
                        'incorrect int_ipv6')
        self.assertIsInstance(system.int_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect int_ipv6')
        self.assertEqual(system.int_ipv6.prefixlen, 128,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv6.ip.compressed, '2a:2a::2a',
                        'incorrect int_ipv6')

    def test_int_ipv6_masked(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a/100')
        self.assertIsInstance(system.int_ipv6, ipaddr.IPv6Network,
                        'incorrect int_ipv6')
        self.assertIsInstance(system.int_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect int_ipv6')
        self.assertEqual(system.int_ipv6.prefixlen, 100,
                        'incorrect int_ipv4')
        self.assertEqual(system.int_ipv6.ip.compressed, '2a:2a::2a',
                        'incorrect int_ipv6')

    def test_lo_ipv4(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a/100',
            lo_ipv4='8.8.8.8')
        self.assertIsInstance(system.lo_ipv4, ipaddr.IPv4Network,
                        'incorrect lo_ipv4')
        self.assertIsInstance(system.lo_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv4.prefixlen, 32,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect lo_ipv4')

    def test_lo_ipv4_masked(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a/100',
            lo_ipv4='8.8.8.8/24')
        self.assertIsInstance(system.lo_ipv4, ipaddr.IPv4Network,
                        'incorrect lo_ipv4')
        self.assertIsInstance(system.lo_ipv4.ip, ipaddr.IPv4Address,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv4.prefixlen, 24,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv4.ip.compressed, '8.8.8.8',
                        'incorrect lo_ipv4')

    def test_lo_ipv6(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a/100',
            lo_ipv6='2a:2a::3a')
        self.assertIsInstance(system.lo_ipv6, ipaddr.IPv6Network,
                        'incorrect lo_ipv6')
        self.assertIsInstance(system.lo_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect lo_ipv6')
        self.assertEqual(system.lo_ipv6.prefixlen, 128,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv6.ip.compressed, '2a:2a::3a',
                        'incorrect lo_ipv6')

    def test_lo_ipv6_masked(self):
        system = self.system_class('system', int_ipv6='2a:2a::2a/100',
            lo_ipv6='2a:2a::3a/100')
        self.assertIsInstance(system.lo_ipv6, ipaddr.IPv6Network,
                        'incorrect lo_ipv6')
        self.assertIsInstance(system.lo_ipv6.ip, ipaddr.IPv6Address,
                        'incorrect lo_ipv6')
        self.assertEqual(system.lo_ipv6.prefixlen, 100,
                        'incorrect lo_ipv4')
        self.assertEqual(system.lo_ipv6.ip.compressed, '2a:2a::3a',
                        'incorrect lo_ipv6')


class MasterTestCase(SystemTestCase):
    system_class = Master

    def test_default_jail_root(self):
        system = self.system_class('system')
        self.assertEqual(system.jail_root, unipath.Path('/usr/jails'),
                         'incorrect default jail_root')

    def test_custom_jail_root(self):
        path = '/usr/local/ezjail'
        system = self.system_class('system', jail_root_path=path)
        self.assertEqual(system.jail_root, unipath.Path(path),
                         'incorrect custom jail_root')

    def test_jlo_if(self):
        system = self.system_class('system', lo_if='lo0')
        self.assertEqual(system.lo_if, 'lo0',
                        'incorrect lo_if')

    def test_jails_dict(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail_1 = Jail('jail_1', master=master, ext_ipv4='7.7.7.7/24')
        jail_2= Jail('jail_2', master=master, ext_ipv4='8.8.8.8/24')
        self.assertDictEqual(master.jails, {jail_1.name: jail_1, jail_2.name: jail_2},
                        'incorrect jails dict')

    def test_add_jail_master(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = self.system_class('jail', ext_ipv4='8.8.8.8/24')
        with self.assertRaises(EzjailError) as cm:
            _jail = master.clone(jail)
        self.assertEqual(cm.exception.message, u'{} should be an instance of systems.Jail'.format(jail.name))

    def test_add_jail_name_in_jails(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertIn('jail', master.jails,
                        'master.jails should have a \'jail\' key')

    def test_add_jail_new(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertNotEqual(_jail, jail,
                        'jail and _jail should be different objects')

    def test_add_jail_not_new(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', master=master, ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertEqual(_jail, jail,
                        'jail and _jail should be the same object')

    def test_add_jail_jails(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertEqual(len(master.jails), 1,
                        'corrupt master.jails')

    def test_add_jail_ip_pool(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertSetEqual(master.ip_pool, set(['9.9.9.9', '8.8.8.8']),
                        'incorrect master ip_pool')

    def test_add_jail_jail_ip_pool(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertSetEqual(_jail.ip_pool, set(['8.8.8.8']),
                        'incorrect jail ip_pool')

    def test_add_jail_if(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertEqual(_jail.ext_if, 're0',
                        'incorrect ext_if')

    def test_add_jail_path(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertEqual(_jail.path, master.jail_root.child(_jail.name),
                        'incorrect jail path')
        self.assertEqual(str(_jail.path), '/usr/jails/jail',
                        'incorrect jail path')

    def test_clone_return(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.assertEqual(_jail, master.jails['jail'],
                        'incorrect jail path')

    def test_add_jail_omnipotency_1(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.expected_values(master, _jail)

    def test_add_jail_omnipotency_3(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = Jail('jail', master=master, ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail)
        self.expected_values(master, _jail)

    def test_add_jail_omnipotency_5(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail_1 = Jail('jail', ext_ipv4='8.8.8.8/24')
        jail_2 = Jail('jail', ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail_1)
        _jail = master.clone(jail_2)
        self.expected_values(master, _jail)

    def test_add_jail_omnipotency_6(self):
        master = self.system_class('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail_1 = Jail('jail', master=master, ext_ipv4='8.8.8.8/24')
        jail_2 = Jail('jail', master=master, ext_ipv4='8.8.8.8/24')
        _jail = master.clone(jail_1)
        self.assertEqual(jail_1, jail_2,
                        'jail_2 and jail_1 should be the same object')
        self.assertEqual(jail_1, _jail,
                        'jail_2 and jail_1 should be the same object')
        self.expected_values(master, jail_1)

    def expected_values(self, master, jail):
        self.assertDictEqual(master.jails, {jail.name: jail},
                        'corrupt master.jails')
        self.assertSetEqual(master.ip_pool, set(['9.9.9.9', '8.8.8.8']),
                        'incorrect master ip_pool')
        self.assertSetEqual(jail.ip_pool, set(['8.8.8.8']),
                        'incorrect jail ip_pool')
        self.assertEqual(jail.ext_if, 're0',
                        'incorrect ext_if')
        self.assertEqual(jail.path, master.jail_root.child(jail.name),
                        'incorrect jail path')
        self.assertEqual(str(jail.path), '/usr/jails/jail',
                        'incorrect jail path')


class DummyMasterTestCase(MasterTestCase):
    system_class = DummyMaster


class JailTestCase(SystemTestCase):
    system_class = Jail

    def test_empty_ip_pool(self):
        jail = self.system_class('jail')
        self.assertSetEqual(jail.ip_pool, set(),
                        'incorrect ip_pool')

    def test_ip_pool(self):
        jail = self.system_class('jail', ext_ipv4='8.8.8.8/24')
        self.assertSetEqual(jail.ip_pool, set(['8.8.8.8']),
                        'incorrect ip_pool')

    def test_ip_pool_2(self):
        jail = self.system_class('jail', ext_ipv4='8.8.8.8/24',
            int_ipv4='8.8.8.9/24')
        self.assertSetEqual(jail.ip_pool, set(['8.8.8.8', '8.8.8.9']),
                        'incorrect ip_pool')

    def test_non_duplicate_master_ip(self):
        master = DummyMaster('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = self.system_class('jail', master=master, ext_ipv4='8.8.8.8/24',
            int_ipv4='8.8.8.9/24')
        self.assertSetEqual(jail.master.ip_pool, set(['9.9.9.9', '8.8.8.8', '8.8.8.9']),
                        'incorrect ip_pool')
        self.assertSetEqual(jail.ip_pool, set(['8.8.8.8', '8.8.8.9']),
                        'incorrect ip_pool')

    def test_duplicate_master_ip(self):
        master = DummyMaster('master', ext_if='re0', ext_ipv4='9.9.9.9')
        with self.assertRaises(EzjailError) as cm:
            jail = self.system_class('jail', master=master, ext_ipv4='8.8.8.8/24',
                int_ipv4='9.9.9.9/24')
        self.assertEqual(cm.exception.message, u'Already attributed IPs: [9.9.9.9]')
        self.assertSetEqual(master.ip_pool, set(['9.9.9.9']),
                        'incorrect ip_pool')

    def test_none_master(self):
        jail = self.system_class('jail', ext_ipv4='8.8.8.8')
        self.assertEqual(jail.master, None,
                        'incorrect master')

    def test_correct_master(self):
        master = DummyMaster('system', ext_if='re0')
        jail = self.system_class('jail', master=master, ext_ipv4='9.9.9.9')
        self.assertEqual(jail.master, master,
                        'incorrect master')

    def test_incorrect_master(self):
        master = System('master', ext_if='re0')
        with self.assertRaises(EzjailError) as cm:
            jail = self.system_class('jail', master=master, ext_ipv4='9.9.9.9')
        self.assertEqual(cm.exception.message, u'master should be an instance of systems.Master')

    def test_ext_if(self):
        with self.assertRaises(EzjailError) as cm:
            super(JailTestCase, self).test_ext_if()
        self.assertEqual(cm.exception.message, u'A Jail cannot define its own interfaces')

    def test_int_if(self):
        with self.assertRaises(EzjailError) as cm:
            super(JailTestCase, self).test_int_if()
        self.assertEqual(cm.exception.message, u'A Jail cannot define its own interfaces')

    def test_lo_if(self):
        with self.assertRaises(EzjailError) as cm:
            super(JailTestCase, self).test_lo_if()
        self.assertEqual(cm.exception.message, u'A Jail cannot define its own interfaces')

    def test_ext_if_2(self):
        master = DummyMaster('master', ext_if='re0')
        jail = self.system_class('jail', master=master)
        self.assertEqual(jail.ext_if, 're0',
                        'incorrect ext_if')

    def test_int_if_2(self):
        master = DummyMaster('master', int_if='re0')
        jail = self.system_class('jail', master=master)
        self.assertEqual(jail.int_if, 're0',
                        'incorrect int_if')

    def test_lo_if_2(self):
        master = DummyMaster('master', lo_if='re0')
        jail = self.system_class('jail', master=master)
        self.assertEqual(jail.lo_if, 're0',
                        'incorrect lo_if')

    def test_no_ext_if(self):
        jail = self.system_class('jail')
        self.assertEqual(jail.ext_if, None,
                        'incorrect ext_if')

    def test_no_int_if(self):
        jail = self.system_class('jail')
        self.assertEqual(jail.int_if, None,
                        'incorrect int_if')

    def test_no_lo_if(self):
        jail = self.system_class('jail')
        self.assertEqual(jail.lo_if, None,
                        'incorrect lo_if')

    # MAIN IP IS DEFINED
    ### IT IS AN ALLOWED MAIN IP
    ###### IT HAS A VALUE IN KWARGS
    def test_custom_main_ip(self):
        jail = self.system_class('jail', ext_ipv4='8.8.8.8',
            int_ipv6='2a:2a::2a', main_ip='int_ipv6')
        self.assertEqual(jail.ip, jail.int_ipv6,
                        'incorrect main ip type')

    ###### IT DOES NOT HAVE A VALUE IN KWARGS
    def test_missing_custom_main_ip(self):
        with self.assertRaises(EzjailError) as cm:
            jail = self.system_class('jail', ext_ipv4='8.8.8.8',
                int_ipv6='2a:2a::2a', main_ip='ext_ipv6')
        self.assertEqual(cm.exception.message, u'Chosen main ip is not defined')

    ### IT IS NOT AN ALLOWED MAIN IP
    def test_invalid_custom_main_ip(self):
        with self.assertRaises(EzjailError) as cm:
            jail = self.system_class('jail', ext_ipv4='8.8.8.8',
                foo='2a:2a::2a', main_ip='foo')
        self.assertEqual(cm.exception.message, u'Chosen main ip is not allowed')

    # MAIN IP IS NOT DEFINED
    ### DEFAULT IP HAS A VALUE IN KWARGS
    def test_default_main_ip(self):
        """
        by default the first type defined in allowed_main_ips
        """
        jail = self.system_class('jail', ext_ipv4='8.8.8.8',
            int_ipv6='2a:2a::2a')
        self.assertEqual(jail.ip, jail.ext_ipv4,
                        'incorrect main ip type')

    ### DEFAULT IP DOES NOT HAVE A VALUE IN KWARGS
    ###### ONLY ONE IP IS DEFINED
    def test_guessed_main_ip(self):
        jail = self.system_class('jail', int_ipv6='2a:2a::2a')
        self.assertEqual(jail.ip, jail.int_ipv6,
                        'incorrect main ip type')

    ###### MORE THAN ONE IP IS DEFINED
    def test_undetermined_main_ip(self):
        with self.assertRaises(EzjailError) as cm:
            jail = self.system_class('jail', int_ipv4='8.8.8.8',
                int_ipv6='2a:2a::2a')
        self.assertEqual(cm.exception.message, u'Main ip cannot be determined')

    def test_mastered_jail_path(self):
        master = DummyMaster('master', ext_if='re0', ext_ipv4='9.9.9.9')
        jail = self.system_class('jail', master=master, ext_ipv4='8.8.8.8/24',
            int_ipv4='8.8.8.9/24')
        self.assertEqual(jail.path, master.jail_root.child(jail.name),
                        'incorrect jail path')
        self.assertEqual(str(jail.path), '/usr/jails/jail',
                        'incorrect jail path')
