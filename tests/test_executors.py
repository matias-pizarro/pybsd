# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import subprocess
import unittest

from pybsd import Executor, Master

from .utils import extract_message

class TestExecutor(Executor):
    ezjail_admin_list_output = (0,
                    """STA JID  IP              Hostname                       Root Directory\n"""
                    """--- ---- --------------- ------------------------------ ------------------------\n"""
                    """ZR  1    10.0.1.41/24    system             /usr/jails/system\n"""
                    """    1    re0|2a01:4f8:210:41e6::1:41:1/100\n"""
                    """    1    lo1|127.0.1.41/24\n"""
                    """    1    lo1|::1:41/100\n""",
                    '')

    def __call__(self, binary, subcommand, *cmd_args, **kwargs):
        if 'ezjail-admin' in binary:
            if subcommand == 'list':
                return self.ezjail_admin_list_output
            elif subcommand == 'console':
                return (0,
                        'The output of command `{}` in jail `{}`'.format(cmd_args[1], cmd_args[2]),
                        '')


class TestExecutorUnknownHeaders(TestExecutor):
    ezjail_admin_list_output = (0,
                    """STA JOID  IP              Hostname                       Root Directory\n"""
                    """--- ---- --------------- ------------------------------ ------------------------\n"""
                    """ZR  1    10.0.1.41/24    system             /usr/jails/system\n"""
                    """    1    re0|2a01:4f8:210:41e6::1:41:1/100\n"""
                    """    1    lo1|127.0.1.41/24\n"""
                    """    1    lo1|::1:41/100\n""",
                    '')


class TestExecutorShortOutput(TestExecutor):
    ezjail_admin_list_output = (0,
                    """STA JID  IP              Hostname                       Root Directory""",
                    '')


class ExecutorTestCase(unittest.TestCase):

    def test_ls_output(self):
        executor = Executor()
        rc, out, err = executor('ls', 'tests/test_executors')
        self.assertEqual(rc, 0, 'incorrect executor return code')
        self.assertEqual(out.decode('ascii'), 'readme\n', 'incorrect executor stdout')
        self.assertEqual(err.decode('ascii'), '', 'incorrect executor stderr')

    def test_ls_fnf_output(self):
        executor = Executor()
        rc, out, err = executor('ls', 'i/do/not/exist')
        self.assertEqual(rc, 2, 'incorrect executor return code')
        self.assertEqual(out.decode('ascii'), '', 'incorrect executor stdout')
        self.assertEqual(err.decode('ascii'), 'ls: cannot access i/do/not/exist: No such file or directory\n', 'incorrect executor stderr')
