# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging

__logger__ = logging.getLogger('pybsd')


class PyBSDError(Exception):
    """Base PyBSD Exception. It is only used to except any PyBSD error and never raised"""
    msg = None


class MasterJailError(PyBSDError):
    """Base exception for errors involving a master and a jail. It is never raised

    Parameters
    ----------
    master : :py:class:`~pybsd.Master`
        The master
    jail : :py:class:`~pybsd.Jail`
        The jail
    """
    def __init__(self, master, jail):
        super(MasterJailError, self).__init__()
        self.master = master
        self.jail = jail

    def __str__(self):
        """Returns the formatted msg as the string representation of the exception"""
        return self.msg.format(master=repr(self.master), jail=repr(self.jail))

    @property
    def message(self):
        """An alias of __str__, useful for tests"""
        return self.__str__()


class AttachNonJailError(MasterJailError):
    """Error when a master tries to import a non-jail

    Parameters
    ----------
    master : :py:class:`~pybsd.Master`
        The master
    jail : `any`
        The object that was supposed to be attached
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{jail}` is not a jail."
