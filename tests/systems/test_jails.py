# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress
import unittest
import unipath
from pybsd.systems import EzjailError
from pybsd.systems.jails import Jail
from pybsd.systems.masters import Master
from .test_systems import BaseSystemTestCase


class JailTestCase(BaseSystemTestCase):

    system_class = Jail
    master_params = {
        'name': 'master',
        'hostname': 'master.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24']),
        'j_if': ('re0', ['10.0.0.0/24']),
        'jlo_if': ('lo1', ['127.0.1.0/24']),
    }
    master = Master(**master_params)
    params = {
        'name': 'system',
        'uid': 12,
        'hostname': 'system.foo.bar',
        'master': master,
        'jail_type': 'Z',
        'auto_start': True,
    }

    def test_no_uid(self):
        params = self.params.copy()
        del params['uid']
        with self.assertRaises(TypeError):
            self.system = self.system_class(**params)

    def test_uid(self):
        self.assertEqual(self.system.uid, 12,
                        'incorrect uid')

    def test_no_jail_type(self):
        params = self.params.copy()
        del params['jail_type']
        self.system = self.system_class(**params)
        self.assertEqual(self.system.jail_type, None,
                        'incorrect jail_type')

    def test_jail_type(self):
        self.assertEqual(self.system.jail_type, 'Z',
                        'incorrect jail_type')

    def test_no_auto_start(self):
        params = self.params.copy()
        del params['auto_start']
        self.system = self.system_class(**params)
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
        with self.assertRaises(EzjailError) as context_manager:
            self.system.status = 'QR'
        self.assertEqual(context_manager.exception.message, u'`QR` is not a valid status (it must be one of R, A or S)')

    def test_jid(self):
        self.assertEqual(self.system.jid, None,
                        'incorrect jid')

    def test_jid_assignement(self):
        self.system.jid = 13
        self.assertEqual(self.system.jid, 13,
                        'incorrect jid')

    def test_jid_failed_assignement(self):
        with self.assertRaises(EzjailError) as context_manager:
            self.system.jid = 'QR'
        self.assertEqual(context_manager.exception.message, u'`QR` is not a valid jid (it must be an integer)')

    @unittest.skip('This cannot be tested until jails have a master')
    def test_path(self):
        self.assertEqual(self.system.path, unipath.Path('/usr/jails/system'),
                        'incorrect path')

    @unittest.skip('This cannot be tested until jails have a master')
    def test_ext_if_name(self):
        self.assertEqual(self.system.ext_if.name, 're0',
                        'incorrect ext_if name')

    @unittest.skip('This cannot be tested until jails have a master')
    def test_ext_if_ifsv4(self):
        self.assertSequenceEqual(self.system.ext_if.ifsv4, [ipaddress.IPv4Interface('10.0.0.0/24')],
                        'incorrect ext_if ifsv4')
        self.assertSequenceEqual(self.system.ext_if.ifsv6, [],
                        'incorrect ext_if ifsv6')

    def test_ext_if_failed_assignement(self):
        with self.assertRaises(EzjailError) as context_manager:
            self.system.ext_if = ('re0', ['8.8.8.8/24'])
        self.assertEqual(context_manager.exception.message, u'Jail interfaces cannot be directly set')

    @unittest.skip('This cannot be tested until jails have a master')
    def test_lo_if_name(self):
        self.assertEqual(self.system.lo_if.name, 'lo1',
                        'incorrect lo_if name')

    @unittest.skip('This cannot be tested until jails have a master')
    def test_lo_if_ifsv4(self):
        self.assertSequenceEqual(self.system.lo_if.ifsv4, [ipaddress.IPv4Interface('127.0.1.0/24')],
                        'incorrect lo_if ifsv4')
        self.assertSequenceEqual(self.system.lo_if.ifsv6, [],
                        'incorrect lo_if ifsv6')

    def test_lo_if_failed_assignement(self):
        with self.assertRaises(EzjailError) as context_manager:
            self.system.lo_if = ('re0', ['8.8.8.8/24'])
        self.assertEqual(context_manager.exception.message, u'Jail interfaces cannot be directly set')
