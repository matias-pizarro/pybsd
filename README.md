# PyBSD #

Provisioning, keeping in sync and maintaining even a medium-sized pool of [FreeBSD](https://www.freebsd.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/freebsd/freebsd) boxes and jails can quickly become a time-consuming and complex task. Tools like [Ansible](http://ansible.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/ansible/ansible), [Fabric](http://www.fabfile.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/fabric/fabric) and [ezjail](http://erdgeist.org/arts/software/ezjail/) [[source](http://erdgeist.org/gitweb/ezjail/)] provide welcome help in one aspect or another and it makes sense to integrate them into a [<img src="https://cloud.githubusercontent.com/assets/644815/8838883/aec0b5b6-30d0-11e5-8f36-3bd9346149f7.png" alt="source"/>](https://hg.python.org/) [Python](https://www.python.org/)-based interface that allows centralized, push-oriented and automated interaction.

A project like [bsdploy](https://github.com/ployground/bsdploy) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/ployground/bsdploy) already leverages these tools to great effect albeit in a very inflexible way that cannot easily be applied to an existing deployment. PyBSD-Project aims at providing a fully customizable Python tool that can be used to maintain an existing array of servers as well as set one up and at making available as well as safely, easily and quickly deployable a wide array of pre-configured, clonable and configurable jails to implement, in a DevOps spirit, tools such as:

   * [nginx](http://nginx.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](http://hg.nginx.org/nginx)
   * [Django](https://www.djangoproject.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/django/django)
   * [Flask](http://flask.pocoo.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/mitsuhiko/flask)
   * [JSON Web Tokens](https://en.wikipedia.org/wiki/JSON_Web_Token) [[libraries]](http://jwt.io/#libraries)
   * [NodeJS](http://nodejs.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/joyent/node) / [io.js](https://iojs.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/nodejs/io.js)
   * [Grunt](http://gruntjs.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/gruntjs/grunt), [Bower](http://bower.io) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/bower/bower) and [Gulp](http://gulpjs.com) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/gulpjs/gulp)
   * [PostgreSQL](http://www.postgresql.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/postgres/postgres)
   * [MySQL](http://www.mysql.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/mysql/mysql-server) / [MariaDB](http://mariadb.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/MariaDB/server) / [Percona](https://www.percona.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8840287/4f5e3d64-30df-11e5-94b4-d8a12efb7eb3.png" alt="source"/>](https://launchpad.net/percona-xtrabackup)
   * [Redis](http://redis.io) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/antirez/redis)
   * [mongoDB](http://www.mongodb.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/mongodb/mongo)
   * [Memcached](http://memcached.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/memcached/memcached)
   * [Solr](http://lucene.apache.org/solr/) [source](http://archive.apache.org/dist/lucene/solr/)
   * [Elasticsearch](https://www.elastic.co/products/elasticsearch) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/elastic/elasticsearch)
   * [Varnish](https://www.varnish-cache.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/varnish/Varnish-Cache)
   * [HaProxy](http://www.haproxy.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/haproxy/haproxy)
   * [Jenkins](http://jenkins-ci.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/jenkinsci/jenkins/)
   * [Sentry](https://getsentry.com) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/getsentry/sentry)
   * [statsd](https://github.com/etsy/statsd) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/etsy/statsd) + [collectd](http://collectd.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/collectd/collectd) + [Graphite](http://graphite.readthedocs.org/en/latest/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/graphite-project/graphite-web)
   * [logstash](https://www.elastic.co/products/logstash) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/elastic/logstash)
   * [InfluxDB](http://influxdb.com) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/influxdb/influxdb)
   * [Grafana](http://grafana.org) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/grafana/grafana)
   * [Pypi](https://pypi.python.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8838883/aec0b5b6-30d0-11e5-8f36-3bd9346149f7.png" alt="source"/>](https://bitbucket.org/pypa/pypi)
   * [Gitolite](http://wiki.github.com/sitaramc/gitolite/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/sitaramc/gitolite)
   * [RabbitMQ](https://www.rabbitmq.com/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/rabbitmq/rabbitmq-server)
   * [poudriere](https://github.com/freebsd/poudriere/wiki) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/freebsd/poudriere)
   * [Let's Encrypt](https://letsencrypt.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/letsencrypt/letsencrypt)
   * [Postfix](http://www.postfix.org/) [[source]](http://www.postfix.org/download.html) + [Dovecot](http://www.dovecot.org/) [<img src="https://cloud.githubusercontent.com/assets/644815/8838883/aec0b5b6-30d0-11e5-8f36-3bd9346149f7.png" alt="source"/>](http://hg.dovecot.org/) + [amavis](http://www.ijs.si/software/amavisd/) [[source]](http://www.ijs.si/software/amavisd/amavisd-new.tar.gz) + [SpamAssassin](http://spamassassin.apache.org) [<img src="https://cloud.githubusercontent.com/assets/644815/8840286/4f465dc0-30df-11e5-8748-b27a79ae8353.png" alt="source"/>](http://wiki.apache.org/spamassassin/DownloadFromSvn)

Somewhere down the line interfacing with [tsuru](https://tsuru.io/) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/tsuru/tsuru) or an equivalent is a goal. On the other hand, once the above shopping list is completed, [Docker](http://www.docker.com) [<img src="https://cloud.githubusercontent.com/assets/644815/8814137/862c35b6-3009-11e5-9260-7bc6ec22ab1c.png" alt="source"/>](https://github.com/docker/docker) on FreeBSD will probably be a reality 8P.

Example:


    >>> from pybsd_project import box_01
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

    python -m unittest discover pybsd.systems
