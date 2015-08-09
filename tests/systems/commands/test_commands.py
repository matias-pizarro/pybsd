# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from pybsd.systems.commands import BaseCommand
from ... import extract_message
from ..test_masters import TestMaster


class NoNameCommand(BaseCommand):
    pass


class NoBinaryCommand(BaseCommand):
    name = 'command_name'


class BaseCommandTestCase(unittest.TestCase):

    params = {
        'name': 'system',
        'hostname': 'system.foo.bar',
        'ext_if': ('re0', ['8.8.8.8/24']),
        'int_if': ('eth0', ['192.168.0.0/24'])
    }

    def setUp(self):
        self.system = TestMaster(**self.params)

    def test_no_name_command(self):
        with self.assertRaises(SystemError) as context_manager:
            NoNameCommand(env='something')
        self.assertEqual(extract_message(context_manager), u'`name` property is missing')

    def test_env_no_executor(self):
        with self.assertRaises(SystemError) as context_manager:
            NoBinaryCommand(env='something')
        self.assertEqual(extract_message(context_manager), u'`something` must have a callable Executor method')

    def test_env_executor_not_callable(self):
        self.system._exec = None
        with self.assertRaises(SystemError) as context_manager:
            NoBinaryCommand(env='something')
        self.assertEqual(extract_message(context_manager), u'`something` must have a callable Executor method')

    def test_no_binary_command(self):
        _bc = NoBinaryCommand(env=self.system)
        with self.assertRaises(NotImplementedError) as context_manager:
            _bc.invoke()
        self.assertEqual(extract_message(context_manager), u'`command_name` is not implemented on this system')
