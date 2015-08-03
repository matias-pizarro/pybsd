# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import unipath


class BaseJailHandler(object):
    default_jail_root = '/usr/jails'

    def __init__(self, master=None, jail_root=None):
        super(BaseJailHandler, self).__init__()
        self.master = master
        j = jail_root or '/usr/jails'
        self.jail_root = unipath.Path(j)

    def get_jail_path(self, jail):
        return self.jail_root.child(jail.name)
