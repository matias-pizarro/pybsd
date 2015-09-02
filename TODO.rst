In Progress
-----------
    * Add docstrings
    * document tests and release
    * tidy up CI configurations

To do
-----
    * example for each class
    * jail type should be defined at jail attachment-time, by the master or its handler
    * Fix appveyor builds
    * check for complexity once Executor.__call__ has been refactored
        flake8  --max-complexity 10 src
    * Use Makefile ¿?
    * Give jails a uuid
    * Work commits into Changelog
    * Add PyPy3 env
    * Make sure different interfaces can have the same name ('re0' for instance)
      But with a different range of ips, of course
    * implement systems.Master.remove_jail
    * implement a cli script
    * Use Ansible, Fabric, cookiecutter and ezjail-admin to do our nefarious bidding
    * PyBSD can base its view of the world on a config or on an analysis of its current state
    * the results of this analysis can in turn be serialized into a config object
    * once the representation of the world is loaded into memory, PyBSD can interact with it programatically
      or let the user interact directly through it
    * The deployment scenarios we consider for now are:
        * local box
        * remote box
        * Digital Ocean droplet
        * EC2 instance
    * Install and use git-flow
    * Outline quickstart documentation

Done
----
    * Restore tox PyPy, 3.3 and 2.6 envs
    * jail hostname should be defined by its handler, unless forced by jail itself
    * Use custom exceptions instead of SystemError
    * Make Sphinx pick up generated docs
    * Give Master a jif
    * reimplement and rename systems.Master.clone clone_jail
    * reimplement systems.Master.add_jail