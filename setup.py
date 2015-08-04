# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="PyBSD",
    version=read('VERSION'),
    author="Matías Pizarro",
    author_email="matias@pizarro net",
    description=("a Python tool to provision, keep in sync and manage "
                   "FreeBSD boxes and jails."),
    license="BSD",
    keywords="FreeBSD jails provisioning ansible fabric ezjail python",
    url="https://github.com/rebost/pybsd",
    install_requires=[
        'lazy',
        'py2-ipaddress',
        'six',
        'sortedcontainers',
        'Unipath',
    ],
    packages=find_packages(exclude=['tests']),
    long_description=read('utils/README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Unix Shell",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
)
