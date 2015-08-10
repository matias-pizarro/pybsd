# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import unittest
import unipath
from pybsd.systems.jails import Jail
from pybsd.systems.masters import System, Master
from .. import extract_message


class JailTestCase(unittest.TestCase):
    master_params = {
        'name': 'master',
        'hostname': 'master.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24']),
        'j_if': ('re0', ['10.0.0.0/24']),
        'jlo_if': ('lo1', ['127.0.1.0/24']),
    }
    params = {
        'name': 'system',
        'uid': 12,
        'hostname': 'system.foo.bar',
        'master': None,
        'jail_type': 'Z',
        'auto_start': True,
    }

    def setUp(self):
        params = self.params.copy()
        params['master'] = Master(**self.master_params)
        self.system = Jail(**params)

    def test_bad_master(self):
        master_params = self.master_params.copy()
        del master_params['j_if']
        del master_params['jlo_if']
        params = self.params.copy()
        params['master'] = System(**master_params)
        with self.assertRaises(SystemError) as context_manager:
            self.system = Jail(**params)
        self.assertEqual(extract_message(context_manager), u'`master` is not a jail master')

    def test_clone(self):
        jail2 = self.system.master.clone(self.system, 'new_jail', 13)
        self.assertNotEqual(self.system, jail2)

    def test_idempotent_add_jail(self):
        jail2 = self.system.master.add_jail(self.system)
        self.assertEqual(self.system, jail2)

    def test_already_with_another_master(self):
        master2 = Master(name='master2',
                         hostname='master2.foo.bar',
                         ext_if=('re0', ['8.8.8.8/24'])
                         )
        with self.assertRaises(SystemError) as context_manager:
            master2.add_jail(self.system)
        self.assertEqual(extract_message(context_manager), u'Jail `system` is already attached to `master`')

    def test_no_name(self):
        params = self.params.copy()
        del params['name']
        with self.assertRaises(TypeError):
            Jail(**params)

    def test_name(self):
        self.assertEqual(self.system.name, 'system',
                        'incorrect name')

    def test_no_hostname(self):
        params = self.params.copy()
        del params['hostname']
        system = Jail(**params)
        self.assertEqual(system.hostname, 'system',
                        'incorrect hostname')

    def test_hostname(self):
        self.assertEqual(self.system.hostname, 'system.foo.bar',
                        'incorrect hostname')

    def test_no_uid(self):
        params = self.params.copy()
        del params['uid']
        with self.assertRaises(TypeError):
            self.system = Jail(**params)

    def test_uid(self):
        self.assertEqual(self.system.uid, 12,
                        'incorrect uid')

    def test_no_jail_type(self):
        params = self.params.copy()
        del params['jail_type']
        self.system = Jail(**params)
        self.assertEqual(self.system.jail_type, None,
                        'incorrect jail_type')

    def test_jail_type(self):
        self.assertEqual(self.system.jail_type, 'Z',
                        'incorrect jail_type')

    def test_no_auto_start(self):
        params = self.params.copy()
        del params['auto_start']
        self.system = Jail(**params)
        self.assertEqual(self.system.auto_start, False,
                        'incorrect auto_start')

    def test_auto_start(self):
        self.assertEqual(self.system.auto_start, True,
                        'incorrect auto_start')

    def test_status(self):
        self.assertEqual(self.system.status, 'S',
                        'incorrect status')

    def test_status_assignement(self):
        self.system.status = 'R'
        self.assertEqual(self.system.status, 'R',
                        'incorrect status')

    def test_status_failed_assignement(self):
        with self.assertRaises(SystemError) as context_manager:
            self.system.status = 'QR'
        self.assertEqual(extract_message(context_manager), u'`QR` is not a valid status (it must be one of R, A or S)')

    def test_jid(self):
        self.assertEqual(self.system.jid, None,
                        'incorrect jid')

    def test_jid_assignement(self):
        self.system.jid = 13
        self.assertEqual(self.system.jid, 13,
                        'incorrect jid')

    def test_jid_failed_assignement(self):
        with self.assertRaises(SystemError) as context_manager:
            self.system.jid = 'QR'
        self.assertEqual(extract_message(context_manager), u'`QR` is not a valid jid (it must be an integer)')

    def test_no_master_path(self):
        params = self.params.copy()
        del params['master']
        self.system = Jail(**params)
        self.assertEqual(self.system.path, None,
                        'incorrect path')

    def test_path(self):
        self.assertEqual(self.system.path, unipath.Path('/usr/jails/system'),
                        'incorrect path')

    def test_no_master_ext_if(self):
        params = self.params.copy()
        del params['master']
        self.system = Jail(**params)
        self.assertEqual(self.system.ext_if, None,
                        'incorrect ext_if')

    def test_ext_if_name(self):
        self.assertEqual(self.system.ext_if.name, 're0',
                        'incorrect ext_if name')

    def test_ext_if_ifsv4(self):
        self.assertSequenceEqual(self.system.ext_if.ifsv4, [ipaddress.IPv4Interface('10.0.0.0/24')],
                        'incorrect ext_if ifsv4')
        self.assertSequenceEqual(self.system.ext_if.ifsv6, [],
                        'incorrect ext_if ifsv6')

    def test_ext_if_failed_assignement(self):
        with self.assertRaises(SystemError) as context_manager:
            self.system.ext_if = ('re0', ['8.8.8.8/24'])
        self.assertEqual(extract_message(context_manager), u'Jail interfaces cannot be directly set')

    def test_no_master_lo_if(self):
        params = self.params.copy()
        del params['master']
        self.system = Jail(**params)
        self.assertEqual(self.system.lo_if, None,
                        'incorrect lo_if')

    def test_lo_if_name(self):
        self.assertEqual(self.system.lo_if.name, 'lo1',
                        'incorrect lo_if name')

    def test_lo_if_ifsv4(self):
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.1.0/24')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [],
                        'incorrect lo_if ifsv6')

    def test_lo_if_failed_assignement(self):
        with self.assertRaises(SystemError) as context_manager:
            self.system.lo_if = ('re0', ['8.8.8.8/24'])
        self.assertEqual(extract_message(context_manager), u'Jail interfaces cannot be directly set')
