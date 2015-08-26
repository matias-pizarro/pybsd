# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from ..utils import extract_message
from .test_base import BaseCommandTestCase


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
        with self.assertRaises(SystemError) as context_manager:
            self.system.ezjail_admin.console(cmd, jail_name)
        message = u'The value `{}` of kwarg `{}` contains whitespace'.format(jail_name, 'jail_name')
        self.assertEqual(extract_message(context_manager), message)
