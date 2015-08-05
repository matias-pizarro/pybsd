=====
PyBSD
=====

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        | |coveralls| |codecov| |landscape| |scrutinizer|
    * - package
      - |version| |downloads|

.. |docs| image:: https://readthedocs.org/projects/pybsd/badge/?style=flat
    :target: https://readthedocs.org/projects/pybsd
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/rebost/pybsd/master.svg?style=flat&label=Travis
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/rebost/pybsd

.. |appveyor| image:: https://img.shields.io/appveyor/ci/rebost/pybsd/master.svg?style=flat&label=AppVeyor
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/rebost/pybsd

.. |coveralls| image:: http://img.shields.io/coveralls/rebost/pybsd/master.svg?style=flat&label=Coveralls
    :alt: Coverage Status
    :target: https://coveralls.io/r/rebost/pybsd


.. |codecov| image:: http://img.shields.io/codecov/c/github/rebost/pybsd/master.svg?style=flat&label=Codecov
    :alt: Coverage Status
    :target: https://codecov.io/github/rebost/pybsd


.. |landscape| image:: https://landscape.io/github/rebost/pybsd/master/landscape.svg?style=flat
    :target: https://landscape.io/github/rebost/pybsd/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/pybsd.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/PyBSD

.. |downloads| image:: http://img.shields.io/pypi/dm/pybsd.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/PyBSD

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/rebost/pybsd/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/rebost/pybsd/

a Python tool to provision, keep in sync and manage FreeBSD boxes and jails

* Free software: BSD license

Provisioning, keeping in sync and maintaining even a medium-sized pool of `FreeBSD <https://www.freebsd.org/>`_ boxes and jails can quickly become a time-consuming and complex task. Tools like `Ansible <http://www.ansible.com/home>`_ , `Fabric <http://www.fabfile.org/>`_ and `ezjail <http://erdgeist.org/arts/software/ezjail/>`_ provide welcome help in one aspect or another and it makes sense to integrate them into a `Python <https://www.python.org/>`_-based interface that allows centralized, push-oriented and automated interaction.

A project like `bsdploy <https://github.com/ployground/bsdploy>`_ already leverages these tools to great effect albeit in a very inflexible way that cannot easily be applied to an existing deployment. PyBSD-Project aims at providing a fully customizable Python tool that can be used to maintain an existing array of servers as well as set one up and at making available as well as safely, easily and quickly deployable a wide array of pre-configured, clonable and configurable jails to implement, in a DevOps spirit, tools such as:

* `nginx <http://nginx.org/>`_
* `Django <https://www.djangoproject.com/>`_
* `Flask <http://flask.pocoo.org/>`_
* `JSON Web Tokens <https://en.wikipedia.org/wiki/JSON_Web_Token>`_
* `NodeJS <https://nodejs.org/>`_ / `io.js <https://iojs.org/>`_
* `Grunt <http://gruntjs.com/>`_ , `Bower <http://bower.io>`_ and `Gulp <http://gulpjs.com>`_
* `PostgreSQL <http://www.postgresql.org/>`_
* `MySQL <http://www.mysql.com/>`_ / `MariaDB <https://mariadb.org/>`_ / `Percona <https://www.percona.com/>`_
* `Redis <http://redis.io>`_
* `mongoDB <https://www.mongodb.org/>`_
* `Memcached <http://memcached.org/>`_
* `Solr <http://lucene.apache.org/solr/>`_
* `Elasticsearch <https://www.elastic.co/products/elasticsearch>`_
* `Varnish <https://www.varnish-cache.org/>`_
* `HaProxy <http://www.haproxy.org/>`_
* `Jenkins <http://jenkins-ci.org/>`_
* `Sentry <https://getsentry.com/welcome/>`_
* `statsd <https://github.com/etsy/statsd>`_ + `collectd <http://collectd.org/>`_ + `Graphite <http://graphite.readthedocs.org/en/latest/>`_
* `logstash <https://www.elastic.co/products/logstash>`_
* `InfluxDB <https://influxdb.com>`_
* `Grafana <http://grafana.org>`_
* `Pypi <https://pypi.python.org/pypi>`_
* `Gitolite <https://github.com/sitaramc/gitolite/wiki>`_
* `RabbitMQ <https://www.rabbitmq.com/>`_
* `poudriere <https://github.com/freebsd/poudriere/wiki>`_
* `Let's Encrypt <https://letsencrypt.org/>`_
* `Postfix <http://www.postfix.org/>`_ + `Dovecot <http://www.dovecot.org/>`_ + `amavis <http://www.ijs.si/software/amavisd/>`_ + `SpamAssassin <http://spamassassin.apache.org>`_

Somewhere down the line interfacing with `tsuru <https://tsuru.io/>`_ or an equivalent is a goal. On the other hand, once the above shopping list is completed, `Docker <https://www.docker.com/>`_ on FreeBSD will probably be a reality 8P.

Installation
============

::

    pip install pybsd

Documentation
=============

https://pybsd.readthedocs.org/

Development
===========

To run the all tests run::

    py.test --pdb
    # or
    tox
