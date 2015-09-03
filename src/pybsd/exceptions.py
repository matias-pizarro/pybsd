# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

__logger__ = logging.getLogger('pybsd')


class PyBSDError(Exception):
    """Base PyBSD Exception. It is only used to except any PyBSD error and never raised

    Attributes
    ----------
    msg : :py:class:`str`
        The template used to generate the exception message
    """
    msg = ''
    parameters = {}

    @property
    def message(self):
        """An alias of __str__, useful for tests"""
        return self.__str__()

    def __str__(self):
        # Returns the formatted msg as the string representation of the exception
        return self.msg.format(**self.parameters)


class InterfaceError(PyBSDError):
    """Base exception for errors involving a network interface.

    Parameters
    ----------
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    interface : :py:class:`~pybsd.network.Interface`
        The interface
    ips : :py:class:`set`
        The ips
    """
    msg = "Can't assign ip(s) `[{ips}]` to `{interface}` on `{environment}`, already in use."

    def __init__(self, environment, interface, ips):
        super(InterfaceError, self).__init__()
        ips_string = ', '.join(ips)
        self.parameters = {'environment': environment, 'interface': interface, 'ips': ips_string}


class BaseCommandError(PyBSDError):
    """Base exception for errors involving a command. It is never raised

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    def __init__(self, command, environment):
        super(BaseCommandError, self).__init__()
        self.parameters = {'command': command, 'environment': environment}


class InvalidCommandNameError(BaseCommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't initialize command: `{command.__class__.__module__}` is missing a `name` property."


class InvalidCommandExecutorError(BaseCommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    """
    msg = "Can't initialize command: `{command}` must have a callable `Executor` method."


class CommandNotImplementedError(BaseCommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't execute command: `{command}` is not implemented on `{environment}`."


class CommandConnectionError(BaseCommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't execute command: `{command}`- can't connect to `{environment}`."


class CommandError(BaseCommandError):
    """Base exception for errors involving a validated command. It is never raised

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    subcommand : :py:class:`str`
        The subcommand, if any
    """
    def __init__(self, command, environment, subcommand=None):
        super(CommandError, self).__init__(command, environment)
        if subcommand:
            command = "{command}[{subcommand}]"
        self.parameters = {'command': command, 'environment': environment}


class WhitespaceError(CommandError):
    """Error when a command arguments include corrupting whitespace

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is executed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    subcommand : :py:class:`str`
        The subcommand, if any
    """
    msg = "`{command}` on `{environment}`: value `{value}` of argument `{argument}` contains whitespace"

    def __init__(self, command, environment, argument, value, subcommand=None):
        super(WhitespaceError, self).__init__(command, environment, subcommand)
        self.parameters = {'command': command, 'environment': environment, 'argument': argument, 'value': value}


class InvalidOutputError(CommandError):
    """Base exception for commands returning invalid output

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is executed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    subcommand : :py:class:`str`
        The subcommand, if any
    err : :py:class:`str`
        The error returned by the subprocess
    """
    msg = "`{command}` on `{environment}` returned: '{err}'"

    def __init__(self, command, environment, err, subcommand=None):
        super(InvalidOutputError, self).__init__(command, environment, subcommand)
        self.parameters = {'command': command, 'environment': environment, 'err': err}


class SubprocessError(CommandError):
    """Base exception for errors returned by a subprocess

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.BaseCommand`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is executed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    subcommand : :py:class:`str`
        The subcommand, if any
    err : :py:class:`str`
        The error returned by the subprocess
    """
    msg = "`{command}` on `{environment}` returned: '{err}'"

    def __init__(self, command, environment, err, subcommand=None):
        super(SubprocessError, self).__init__(command, environment, subcommand)
        self.parameters = {'command': command, 'environment': environment, 'err': err}


class MasterJailError(PyBSDError):
    """Base exception for errors involving a master and a jail. It is never raised

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    def __init__(self, master, jail):
        super(MasterJailError, self).__init__()
        self.parameters = {'master': master, 'jail': jail}


class AttachNonMasterError(MasterJailError):
    """Error when a master tries to import a non-jail

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The object that was supposed to host the jail
    jail : `any`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{master}` is not a master."


class AttachNonJailError(MasterJailError):
    """Error when a master tries to import a non-jail

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : `any`
        The object that was supposed to be attached
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{jail}` is not a jail."


class JailAlreadyAttachedError(MasterJailError):
    """Error when a jail is already attached to another master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{jail}` is already attached to `{jail.master}`."


class DuplicateJailNameError(MasterJailError):
    """Error when another jail with the same name is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    duplicate : :py:class:`str`
        The duplicated hostname
    """
    msg = u"Can't attach `{jail}` to `{master}`. Name `{duplicate}` is already associated with `{master}`."

    def __init__(self, master, jail, duplicate):
        super(DuplicateJailNameError, self).__init__(master=master, jail=jail)
        self.parameters['duplicate'] = duplicate


class DuplicateJailHostnameError(DuplicateJailNameError):
    """Error when another jail with the same hostname is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    duplicate : :py:class:`str`
        The duplicated hostname
    """
    msg = u"Can't attach `{jail}` to `{master}`. Hostname `{duplicate}` is already associated with `{master}`."


class DuplicateJailUidError(DuplicateJailNameError):
    """Error when another jail with the same uid is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    duplicate : :py:class:`str`
        The duplicated hostname
    """
    msg = u"Can't attach `{jail}` to `{master}`. A jail with uid `{duplicate}` is already attached to `{master}`."
