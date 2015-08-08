# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import six
import unittest
from pybsd.exceptions import SystemError
from pybsd.systems.commands import BaseCommand, CommandError
from pybsd.systems.masters import DummyMaster


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
        self.system = DummyMaster(**self.params)

    def test_no_name_command(self):
        with self.assertRaises(CommandError) as context_manager:
            _bc = NoNameCommand(env='something')
        self.assertEqual(context_manager.exception.message, u'`name` property is missing')

    def test_env_no_executor(self):
        with self.assertRaises(SystemError) as context_manager:
            _bc = NoBinaryCommand(env='something')
        self.assertEqual(context_manager.exception.message, u'`something` must have a callable Executor method')

    def test_env_executor_not_callable(self):
        self.system._exec = None
        with self.assertRaises(SystemError) as context_manager:
            _bc = NoBinaryCommand(env='something')
        self.assertEqual(context_manager.exception.message, u'`something` must have a callable Executor method')

    def test_no_binary_command(self):
        _bc = NoBinaryCommand(env=self.system)
        with self.assertRaises(NotImplementedError) as context_manager:
            _bc.invoke()
        message = context_manager.exception.message if six.PY2 else context_manager.exception.args[0]
        self.assertEqual(message, u'`command_name` is not implemented on this system')

    # def test_no_binary_command(self):
    #     with self.assertRaises(SystemError) as context_manager:
    #         _bc = NoBinaryCommand(env='something')
    #     self.assertEqual(context_manager.exception.message, u'`something` must have a callable Executor method')
