# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from pybsd.systems import BaseSystem


class BaseSystemTestCase(unittest.TestCase):
    """
    Somewhere down the line, the bleeding obvious comes back to kick our ass
    My bleeding obvious might not be your bleeding obvious
    Somewhere down the line the bleeding obvious might not seem so obvious
    Tests are part of the documentation
    Redundancy in tests is a feature, not an issue
    """
    system_class = BaseSystem
    params = {'name': 'system', 'hostname': 'system.foo.bar'}

    def setUp(self):
        self.system = self.system_class(**self.params)

    def test_no_name(self):
        params = self.params.copy()
        del params['name']
        with self.assertRaises(TypeError):
            self.system_class(**params)

    def test_name(self):
        self.assertEqual(self.system.name, 'system',
                        'incorrect name')

    def test_no_hostname(self):
        params = self.params.copy()
        del params['hostname']
        system = self.system_class(**params)
        self.assertEqual(system.hostname, 'system',
                        'incorrect hostname')

    def test_hostname(self):
        self.assertEqual(self.system.hostname, 'system.foo.bar',
                        'incorrect hostname')
