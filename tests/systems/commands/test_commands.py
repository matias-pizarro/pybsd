# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
from pybsd.systems import System, SystemError
from pybsd.systems.commands import BaseCommand, CommandError


class NoNameCommand(BaseCommand):
    pass

class NoBinaryCommand(BaseCommand):
    name = 'command_name'

class BaseCommandTestCase(unittest.TestCase):

    def test_no_name_command(self):
        with self.assertRaises(CommandError) as context_manager:
            _bc = NoNameCommand(env='something')
        self.assertEqual(context_manager.exception.message, u'`name` property is missing')

    def test_env_executor(self):
        with self.assertRaises(SystemError) as context_manager:
            _bc = NoBinaryCommand(env='something')
        self.assertEqual(context_manager.exception.message, u'`something` must have a callable Executor method')

    # def test_no_binary_command(self):
    #     with self.assertRaises(SystemError) as context_manager:
    #         _bc = NoBinaryCommand(env='something')
    #     self.assertEqual(context_manager.exception.message, u'`something` must have a callable Executor method')
