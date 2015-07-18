# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from . import System, Host, Jail

class SystemTestCase(unittest.TestCase):
    def setUp(self):
        self.system = System('system')

    def tearDown(self):
        self.widget = None

    def test_name(self):
        self.assertEqual(self.system.name, 'system',
                         'incorrect name')


class HostTestCase(SystemTestCase):
    def setUp(self):
        self.system = Host('system')


class JailTestCase(SystemTestCase):
    def setUp(self):
        self.system = Jail('system')
