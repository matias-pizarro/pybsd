# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unittest
import unipath
from pybsd.systems.handlers import BaseJailHandler


class BaseJailHandlerTestCase(unittest.TestCase):

    def test_default_jail_root(self):
        handler = BaseJailHandler()
        self.assertEqual(handler.jail_root, unipath.Path('/usr/jails'),
                        'incorrect jail_root')

    def test_jail_root(self):
        handler = BaseJailHandler(jail_root='/var/jails')
        self.assertEqual(handler.jail_root, unipath.Path('/var/jails'),
                        'incorrect jail_root')

    def test_no_master(self):
        handler = BaseJailHandler()
        self.assertEqual(handler.master, None,
                        'incorrect master')
