Roadmap
=======

All the -- *expected* -- dates of completion and version numbers are pure hypothesis, likely to be modified by reality.

Until version 1.0.0, the API, properties, methods and trheir signature are likely to change a lot.


0.0.3 (expected end of 2015-08)
-------------------------------
**Complete documentation:**

the idea is that keeping documentation up to date is not a realistic prospect until we have the current code base covered.
Further development is therefore put on the backburner until this is achieved.

0.0.4 (expected wk1 of 2015-09)
--------------------------------
**Make all existing methods work with a modelized set up:**

* Some methods depend on interaction with the host, like Jail.status.
* In order to plan and test deployments and architecture we need to be able to work on models without direct interaction with
  existing systems.
* To achieve this, when not working on an actual system, the package will create and maintain internal state that allows
  state-dependent methods to work
* implement Master.remove_jail method

0.0.5 (expected wk2 of 2015-09)
-------------------------------
Check all existing methods correctly work on a local instance

0.0.6 (expected wk3 of 2015-09)
-------------------------------
Make all existing methods work remotely

0.0.7 (expected end of 2015-09)
-------------------------------
**Implement the other methods of EzjailAdmin**

* console
* create
* delete
* start
* stop

0.0.8 (expected wk1 of 2015-10)
-------------------------------
* Serialize to files an existing model

0.0.9 (expected wk2 of 2015-10)
-------------------------------
* Import from files a serialized model

