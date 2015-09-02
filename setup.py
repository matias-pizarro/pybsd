#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
import sys
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

requirements = [
    'lazy',
    'six',
    'sortedcontainers',
    'Unipath',
]
if sys.version_info.major == 2:
    requirements.append('py2-ipaddress')

setup(
    name="PyBSD",
    version='0.0.2',
    license='BSD',
    description='a Python tool to provision, keep in sync and manage FreeBSD boxes and jails',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author="Matías Pizarro",
    author_email='matias@pizarro.net',
    url='https://github.com/rebost/pybsd',
    packages=find_packages('src/pybsd'),
    package_dir={'': 'src/pybsd'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/pybsd/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Unix Shell",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    keywords=[
        'FreeBSD', 'jails', 'provisioning', 'ansible', 'fabric', 'ezjail', 'python',
    ],
    install_requires=requirements,
)
