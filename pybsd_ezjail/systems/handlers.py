# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import ipaddress


class BaseJailHandler(object):
    master = None

    def __init__(self, master):
        super(BaseJailHandler, self).__init__()
        self.master = master

    def get_jail_path(self, jail):
        return self.master.jail_root.child(jail.name)
