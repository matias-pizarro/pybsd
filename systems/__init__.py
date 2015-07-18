# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import


class System(object):
    """Describes an OS instance, as a computer, a virtualized system or a jail"""
    def __init__(self, name):
        super(System, self).__init__()
        self.name = name


class Host(System):
    """Describes a system that will host jails"""
    pass


class Jail(System):
    """Describes a jailed system"""
    pass
