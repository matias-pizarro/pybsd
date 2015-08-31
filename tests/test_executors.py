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
        self.assertEqual(out, 'readme\n', 'incorrect executor stdout')
        self.assertEqual(err, '', 'incorrect executor stderr')

    def test_ls_output_splitlines(self):
        executor = Executor(splitlines=True)
        rc, out, err = executor('ls', 'tests/test_executors')
        self.assertEqual(rc, 0, 'incorrect executor return code')
        self.assertEqual(out, ['readme'], 'incorrect executor stdout')
        self.assertEqual(err, [], 'incorrect executor stderr')

    def test_ls_file_not_found_output(self):
        executor = Executor()
        rc, out, err = executor('ls', 'i/do/not/exist')
        self.assertEqual(rc, 2, 'incorrect executor return code')
        self.assertEqual(out, '', 'incorrect executor stdout')
        self.assertEqual(err, 'ls: cannot access i/do/not/exist: No such file or directory\n', 'incorrect executor stderr')

    def test_ls_with_err_output(self):
        executor = Executor()
        rc, out = executor('ls', 'tests/test_executors', err='')
        self.assertEqual(rc, 0, 'incorrect executor return code')
        self.assertEqual(out, 'readme\n', 'incorrect executor stdout')

    def test_ls_with_out_and_err_output(self):
        executor = Executor()
        rc = executor('ls', 'tests/test_executors', out='readme\n', err='')
        self.assertEqual(rc, 0, 'incorrect executor return code')

    def test_ls_with_rc_out_err_output(self):
        executor = Executor()
        rc = executor('ls', 'tests/test_executors', rc=0, out='readme\n', err='')
        self.assertEqual(rc, None, 'incorrect executor return code')

    def test_ls_calledprocesserror_1(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'tests/test_executors', rc=2, out='readme\n', err='')
        self.assertEqual(context_manager.exception.returncode, 0, 'incorrect executor return code')

    def test_ls_calledprocesserror_2(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'tests/test_executors', rc=0, out='readme\n', err='something')
        self.assertEqual(context_manager.exception.returncode, 0, 'incorrect executor return code')

    def test_ls_calledprocesserror_3(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'i/do/not/exist', rc=2, out='', err='something')
        self.assertEqual(context_manager.exception.returncode, 2, 'incorrect executor return code')

    def test_ls_calledprocesserror_4(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'tests/test_executors', rc=0, out='', err='something')
        self.assertEqual(context_manager.exception.returncode, 0, 'incorrect executor return code')

    def test_ls_calledprocesserror_5(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'i/do/not/exist', rc=2, out='readme\n', err='something')
        self.assertEqual(context_manager.exception.returncode, 2, 'incorrect executor return code')

    def test_ls_calledprocesserror_6(self):
        executor = Executor()
        with self.assertRaises(subprocess.CalledProcessError) as context_manager:
            executor('ls', 'i/do/not/exist', rc=[1, 3], out='readme\n', err='something')
        self.assertEqual(context_manager.exception.returncode, 2, 'incorrect executor return code')
