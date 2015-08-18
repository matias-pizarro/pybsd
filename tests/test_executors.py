# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from pybsd.executors import BaseExecutor


class TestExecutor(BaseExecutor):
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
