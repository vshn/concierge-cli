Concierge-cli |latest-version|
==============================

|build-status| |python-support| |license|

Companion CLI for `Concierge`_, the Configuration management & CI solution
for aligning your multitude of Git repositories.  Allows you to bulk-manage
properties of your Git repository projects.  Currently, GitLab is supported.

.. |latest-version| image:: https://img.shields.io/pypi/v/concierge-cli.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/concierge-cli
.. |build-status| image:: https://img.shields.io/travis/vshn/concierge-cli/master.svg
   :alt: Build status
   :target: https://travis-ci.org/vshn/concierge-cli
.. |python-support| image:: https://img.shields.io/pypi/pyversions/concierge-cli.svg
   :alt: Python versions
   :target: https://pypi.org/project/concierge-cli
.. |license| image:: https://img.shields.io/pypi/l/concierge-cli.svg
   :alt: Software license
   :target: https://github.com/vshn/concierge-cli/blob/master/LICENSE

.. _Concierge: https://hub.docker.com/r/vshn/concierge/

Why Should I Use This Tool?
---------------------------

Concierge-cli helps you analyze and bulk-update the repository projects you
manage (e.g. set topics on projects, generate project lists for ModuleSync).

Installation
------------

From PyPI:

.. code-block:: console

    $ pip install concierge-cli

Usage Patterns
--------------

List all projects (for a private GitLab) that have no topics yet:

.. code-block:: console

    $ concierge-cli gitlab --uri git.vs.hn topics --empty

List all projects "foo" or similar in group "bar" or similar: (on GitLab.com)

.. code-block:: console

    $ concierge-cli gitlab topics bar/foo --empty

Set topics on all those projects:

.. code-block:: console

    $ concierge-cli gitlab topics bar/foo --empty --set-topic Puppet --set-topic Ansible

List all projects *with* topics now: (double-check)

.. code-block:: console

    $ concierge-cli gitlab topics bar/foo

Print a YAML list of all projects matching a topic:

.. code-block:: console

    $ concierge-cli gitlab projects --topic Puppet

Update the list of modules Concierge manages with a specific configuration:

.. code-block:: console

    $ concierge-cli gitlab projects --topic Puppet > configs/foo-bar/managed_modules.yml
    $ git add -v configs/foo-bar/managed_modules.yml
    $ git status && git commit -m 'Added ...' && git push
