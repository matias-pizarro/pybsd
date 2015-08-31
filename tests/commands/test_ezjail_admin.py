# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from pybsd import InvalidOutputError, WhitespaceError

from .test_base import BaseCommandTestCase
from ..test_executors import TestExecutorShortOutput, TestExecutorUnknownHeaders


class EzjailAdminTestCase(BaseCommandTestCase):

    def test_list(self):
        self.assertSequenceEqual(self.system.ezjail_admin.list(),
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

    def test_console(self):
        cmd = 'service'
        jail_name = 'test_jail'
        expected_output = 'The output of command `{}` in jail `{}`'.format(cmd, jail_name)
        self.assertSequenceEqual(self.system.ezjail_admin.console(cmd, jail_name),
                                expected_output,
                                'incorrect ezjail-admin console output')

    def test_catch_whitespace(self):
        cmd = 'service'
        jail_name = 'test jail'
        with self.assertRaises(WhitespaceError) as context_manager:
            self.system.ezjail_admin.console(cmd, jail_name)
        self.assertEqual(context_manager.exception.message,
                         "`ezjail-admin` on `system.foo.bar`: value `test jail` of argument `jail_name` contains whitespace")


class ShortOutputTestCase(BaseCommandTestCase):
    executor_class = TestExecutorShortOutput

    def test_list_too_short(self):
        with self.assertRaises(InvalidOutputError) as context_manager:
            self.system.ezjail_admin.list()
        self.assertEqual(context_manager.exception.message,
                         "`ezjail-admin` on `system.foo.bar` returned: 'output too short'")


class UnknownHeadersTestCase(BaseCommandTestCase):
    executor_class = TestExecutorUnknownHeaders

    def test_unknown_headers(self):
        with self.assertRaises(InvalidOutputError) as context_manager:
            self.system.ezjail_admin.list()
        self.assertEqual(context_manager.exception.message,
                         "`ezjail-admin` on `system.foo.bar` returned: 'output has unknown headers\n['STA', 'JOID', 'IP', 'Hostname', 'Root Directory']'")
