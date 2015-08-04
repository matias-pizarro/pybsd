=====
PyBSD
=====

Provisioning, keeping in sync and maintaining even a medium-sized pool of `FreeBSD <https://www.freebsd.org/>`_ boxes and jails can quickly become a time-consuming and complex task. Tools like `Ansible <http://ansible.com/>`_ , `Fabric <http://www.fabfile.org/>`_ and `ezjail <http://erdgeist.org/arts/software/ezjail/>`_ provide welcome help in one aspect or another and it makes sense to integrate them into a `Python <https://www.python.org/>`_-based interface that allows centralized, push-oriented and automated interaction.

A project like `bsdploy <https://github.com/ployground/bsdploy>`_ already leverages these tools to great effect albeit in a very inflexible way that cannot easily be applied to an existing deployment. PyBSD-Project aims at providing a fully customizable Python tool that can be used to maintain an existing array of servers as well as set one up and at making available as well as safely, easily and quickly deployable a wide array of pre-configured, clonable and configurable jails to implement, in a DevOps spirit, tools such as:

* `nginx <http://nginx.org/>`_
* `Django <https://www.djangoproject.com/>`_
* `Flask <http://flask.pocoo.org/>`_
* `JSON Web Tokens <https://en.wikipedia.org/wiki/JSON_Web_Token>`_
* `NodeJS <http://nodejs.org/>`_ / `io.js <https://iojs.org/>`_
* `Grunt <http://gruntjs.com/>`_ , `Bower <http://bower.io>`_ and `Gulp <http://gulpjs.com>`_
* `PostgreSQL <http://www.postgresql.org/>`_
* `MySQL <http://www.mysql.com/>`_ / `MariaDB <http://mariadb.org/>`_ / `Percona <https://www.percona.com/>`_
* `Redis <http://redis.io>`_
* `mongoDB <http://www.mongodb.org/>`_
* `Memcached <http://memcached.org/>`_
* `Solr <http://lucene.apache.org/solr/>`_
* `Elasticsearch <https://www.elastic.co/products/elasticsearch>`_
* `Varnish <https://www.varnish-cache.org/>`_
* `HaProxy <http://www.haproxy.org/>`_
* `Jenkins <http://jenkins-ci.org/>`_
* `Sentry <https://getsentry.com>`_
* `statsd <https://github.com/etsy/statsd>`_ + `collectd <http://collectd.org/>`_ + `Graphite <http://graphite.readthedocs.org/en/latest/>`_
* `logstash <https://www.elastic.co/products/logstash>`_
* `InfluxDB <http://influxdb.com>`_
* `Grafana <http://grafana.org>`_
* `Pypi <https://pypi.python.org/>`_
* `Gitolite <http://wiki.github.com/sitaramc/gitolite/>`_
* `RabbitMQ <https://www.rabbitmq.com/>`_
* `poudriere <https://github.com/freebsd/poudriere/wiki>`_
* `Let's Encrypt <https://letsencrypt.org/>`_
* `Postfix <http://www.postfix.org/>`_ + `Dovecot <http://www.dovecot.org/>`_ + `amavis <http://www.ijs.si/software/amavisd/>`_ + `SpamAssassin <http://spamassassin.apache.org>`_

Somewhere down the line interfacing with `tsuru <https://tsuru.io/>`_ or an equivalent is a goal. On the other hand, once the above shopping list is completed, `Docker <http://www.docker.com>`_ on FreeBSD will probably be a reality 8P.

Example:


    >>> from pybsd import box_01
    >>> box_01.ezjail_admin('list')
    {
      u'nginx': {
        u'ip': u'10.0.1.41/24',
        u'ips': [
          u'10.0.1.41/24',
          u'2a01:4f8:210:41e6::1:41:1',
          u'127.0.1.41',
          u'::1:41'
        ],
        u'jid': u'1',
        u'root': u'/usr/jails/nginx',
        u'status': u'ZR'
      }
    }


Tests can be run like so:


    python -m unittest discover tests --failfast
    # or
    python tests/run.py
    # or
    tox
