* Use Makefile ¿?
* Make Sphynx pick up generated docs
* Add docstrings
* Work commits into Changelog
* Restore tox PyPy, 3.3 and 2.6 envs
* Give Master aa jif
* Make sure different interfaces can have the same name ('re0' for instance)
  But with a different range of ips, of course
* implement systems.Master.remove_jail
* reimplement and rename systems.Master.clone clone_jail
* reimplement systems.Master.add_jail
* implement a cli script
* document tests and release
* Use Ansible, Fabric, cookiecutter and ezjail-admin to do our nefarious bidding
* PyBSD can base its view of the world on a config or on an analysis of its current state
* the results of trhis analysis can in turn be serialized into a config object
* once the representation of the world is loaded into memory, PyBSD can interact with it programatically
  or let the user interact directly through it
* The deployment scenarios we consider for now are:
    * local box
    * remote box
    * Digital Ocean droplet
    * EC2 instance