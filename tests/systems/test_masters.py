# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import ipaddress

from pybsd import (AttachNonJailError, BaseJailHandler, DuplicateJailHostnameError, DuplicateJailNameError, DuplicateJailUidError,
                   InterfaceError, Jail, JailAlreadyAttachedError, Master)

from .test_base import SystemTestCase


class MasterTestCase(SystemTestCase):

    system_class = Master
    params = {
        'name': 'system',
        'hostname': 'master.foo.bar',
        'ext_if': ('re0', ['148.241.178.106/24', '1c02:4f8:0f0:14e6::/110']),
        'int_if': ('eth0', ['192.168.0.0/24', '1c02:4f8:0f0:14e6::0:0:1/110']),
        # 'lo_if': ('lo0', ['127.0.0.1/24', '::1/110']),
        'j_if': ('re0', ['10.0.2.0/24', '10.0.1.0/24', '1c02:4f8:0f0:14e6::2:0:1/110', '1c02:4f8:0f0:14e6::1:0:1/110']),
        'jlo_if': ('lo1', ['127.0.2.0/24', '127.0.1.0/24', '::0:2:0:0/110', '::0:1:0:0/110']),
    }

    def test_j_if_name(self):
        self.assertEqual(self.system.j_if.name, 're0',
                        'incorrect j_if name')

    def test_j_if_ifsv4(self):
        self.assertSequenceEqual(self.system.j_if.ifsv4, [ipaddress.IPv4Interface('10.0.1.0/24'),
                                                          ipaddress.IPv4Interface('10.0.2.0/24')],
                        'incorrect j_if ifsv4')

    def test_j_if_ifsv6(self):
        self.assertSequenceEqual(self.system.j_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::1:0:1/110'),
                                                          ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::2:0:1/110')],
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
        self.assertSequenceEqual(system.j_if.ifsv4, [ipaddress.IPv4Interface('148.241.178.106/24')],
                        'incorrect j_if ifsv4')
        self.assertSequenceEqual(system.j_if.ifsv6, [ipaddress.IPv6Interface('1c02:4f8:0f0:14e6::/110')],
                        'incorrect j_if ifsv6')

    def test_duplicate_j_if(self):
        params = self.params.copy()
        params['j_if'] = ('re0', ['148.241.178.106/24'])
        with self.assertRaises(InterfaceError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message,
                         "Can't assign ip(s) `[148.241.178.106]` to `re0` on `{}`, already in use.".format(params['name']))

    def test_jlo_if_name(self):
        self.assertEqual(self.system.jlo_if.name, 'lo1',
                        'incorrect jlo_if name')

    def test_jlo_if_ifsv4(self):
        self.assertSequenceEqual(self.system.jlo_if.ifsv4, [ipaddress.IPv4Interface('127.0.1.0/24'),
                                                            ipaddress.IPv4Interface('127.0.2.0/24')],
                        'incorrect jlo_if ifsv4')

    def test_jlo_if_ifsv6(self):
        self.assertSequenceEqual(self.system.jlo_if.ifsv6, [ipaddress.IPv6Interface('::0:1:0:0/110'),
                                                            ipaddress.IPv6Interface('::0:2:0:0/110')],
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
        self.assertSequenceEqual(system.jlo_if.ifsv6, [ipaddress.IPv6Interface('::1/110')],
                        'incorrect jlo_if ifsv6')

    def test_duplicate_jlo_if(self):
        params = self.params.copy()
        params['jlo_if'] = ('lo1', ['127.0.0.1/24'])
        with self.assertRaises(InterfaceError) as context_manager:
            self.system_class(**params)
        self.assertEqual(context_manager.exception.message,
                         "Can't assign ip(s) `[127.0.0.1]` to `lo1` on `{}`, already in use.".format(params['name']))

    def test_jail_handler(self):
        self.assertIsInstance(self.system.jail_handler, BaseJailHandler,
                        'incorrect jail_handler')
        self.assertEqual(self.system.jail_handler.master, self.system,
                        'incorrect jail_handler')

    def test_attach_non_jail(self):
        master2 = Master(name='master2',
                         hostname='master2.foo.bar',
                         ext_if=('re0', ['148.241.178.106/24'])
                         )
        with self.assertRaises(AttachNonJailError) as context_manager:
            self.system.attach_jail(master2)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `{jail.name}` to `{master.name}`. `{jail.name}`"
                         " is not a jail.".format(master=self.system, jail=master2))

    def test_jail_already_attached(self):
        master2 = Master(name='master2',
                         hostname='master2.foo.bar',
                         ext_if=('re0', ['148.241.178.107/24'])
                         )
        jail = Jail(name='jail',
                    uid=12,
                    hostname='jail.foo.bar',
                    master=master2)
        with self.assertRaises(JailAlreadyAttachedError) as context_manager:
            self.system.attach_jail(jail)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `{jail.name}` to `{master1.name}`. `{jail.name}` is already attached"
                         " to `{master2.name}`.".format(master1=self.system, master2=master2, jail=jail))

    def test_duplicate_original_name(self):
        jail = Jail(name='jail1', uid=11, master=self.system)
        with self.assertRaises(DuplicateJailNameError) as context_manager:
            assert Jail(name='jail1', uid=12, master=self.system)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `{jail.name}` to `{master.name}`. Name `{jail.name}` is already associated"
                         " with `{master.name}`.".format(master=self.system, jail=jail))

    def test_duplicate_name(self):
        assert Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail3', uid=12, master=self.system)
        with self.assertRaises(DuplicateJailNameError) as context_manager:
            jail2.name = 'jail1'
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `{jail.name}` to `{master.name}`. Name `jail1` is already associated"
                         " with `{master.name}`.".format(master=self.system, jail=jail2))

    def test_duplicate_orig_hostname(self):
        jail = Jail(name='jail1', hostname='something.foo.bar', uid=11, master=self.system)
        with self.assertRaises(DuplicateJailHostnameError) as context_manager:
            assert Jail(name='jail2', hostname='something.foo.bar', uid=12, master=self.system)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `jail2` to `{master.name}`. Hostname `something.foo.bar`"
                         " is already associated with `{master.name}`.".format(master=self.system, jail=jail))

    def test_duplicate_hostname(self):
        jail = Jail(name='jail1', hostname='something.foo.bar', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        with self.assertRaises(DuplicateJailHostnameError) as context_manager:
            jail2.hostname = 'something.foo.bar'
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `jail2` to `{master.name}`. Hostname `something.foo.bar`"
                         " is already associated with `{master.name}`.".format(master=self.system, jail=jail))

    def test_duplicate_own_hostname(self):
        jail = Jail(name='jail1', hostname='master.foo.bar', uid=11)
        with self.assertRaises(DuplicateJailHostnameError) as context_manager:
            self.system.attach_jail(jail)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `{jail.name}` to `{master.name}`. Hostname `master.foo.bar`"
                         " is already associated with `{master.name}`.".format(master=self.system, jail=jail))

    def test_duplicate_original_uid(self):
        jail = Jail(name='jail1', uid=11, master=self.system)
        with self.assertRaises(DuplicateJailUidError) as context_manager:
            assert Jail(name='jail2', uid=11, master=self.system)
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `jail2` to `{master.name}`. A jail with uid `{jail.uid}` is"
                         " already attached to `{master.name}`.".format(master=self.system, jail=jail))

    def test_duplicate_uid(self):
        jail = Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        with self.assertRaises(DuplicateJailUidError) as context_manager:
            jail2.uid = 11
        self.assertEqual(context_manager.exception.message,
                         "Can't attach `jail2` to `{master.name}`. A jail with uid `{jail.uid}` is"
                         " already attached to `{master.name}`.".format(master=self.system, jail=jail))

    def test_jails_dict(self):
        jail1 = Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        jail3 = Jail(name='jail3', uid=13, master=self.system)
        self.assertDictEqual(self.system.jails, {'jail1': jail1,
                                                 'jail2': jail2,
                                                 'jail3': jail3},
                        'incorrect jails dictionnary')

    def test_names_wo_jails(self):
        self.assertSetEqual(self.system.names, {self.system.name},
                        'incorrect names')

    def test_names_w_jails(self):
        jail1 = Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        jail3 = Jail(name='jail3', uid=13, master=self.system)
        self.assertSetEqual(self.system.names, {self.system.name,
                                                    jail1.name,
                                                    jail2.name,
                                                    jail3.name},
                        'incorrect names')

    def test_hostnames_wo_jails(self):
        self.assertSetEqual(self.system.hostnames, {self.system.hostname},
                        'incorrect hostnames')

    def test_hostnames_w_jails(self):
        jail1 = Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        jail3 = Jail(name='jail3', uid=13, master=self.system)
        self.assertSetEqual(self.system.hostnames, {self.system.hostname,
                                                    jail1.hostname,
                                                    jail2.hostname,
                                                    jail3.hostname},
                        'incorrect hostnames')

    def test_uids_wo_jails(self):
        self.assertSetEqual(self.system.uids, set(),
                        'incorrect uids')

    def test_uids_w_jails(self):
        jail1 = Jail(name='jail1', uid=11, master=self.system)
        jail2 = Jail(name='jail2', uid=12, master=self.system)
        jail3 = Jail(name='jail3', uid=13, master=self.system)
        self.assertSetEqual(self.system.uids, {jail1.uid, jail2.uid, jail3.uid},
                        'incorrect uids')

    def test_ezjail_admin_binary(self):
        self.assertEqual(self.system.ezjail_admin_binary, u'/usr/local/bin/ezjail-admin',
                        'incorrect j_if name')

    def test_reset_j_if(self):
        self.system.reset_j_if()
        self.assertEqual(self.system.j_if, self.system.ext_if,
                        'systems.master.Master.reset_j_if is broken')

    def test_reset_jlo_if(self):
        self.system.reset_jlo_if()
        self.assertEqual(self.system.jlo_if, self.system.lo_if,
                        'systems.master.Master.reset_jlo_if is broken')
