Concierge-cli |latest-version|
==============================

|build-status| |health| |updates| |python-support| |license|

Companion CLI for `Concierge`_, the Configuration management & CI solution
for aligning your multitude of Git repositories.  Allows you to bulk-manage
properties of your Git repository projects.  Currently, GitLab is supported.

.. |latest-version| image:: https://img.shields.io/pypi/v/concierge-cli.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/concierge-cli
.. |build-status| image:: https://img.shields.io/travis/vshn/concierge-cli/master.svg
   :alt: Build status
   :target: https://travis-ci.org/vshn/concierge-cli
.. |health| image:: https://img.shields.io/codacy/grade/363c38ca95b941438b442afb64591892/master.svg
   :target: https://www.codacy.com/app/VSHN/concierge-cli
   :alt: Code health
.. |updates| image:: https://pyup.io/repos/github/vshn/concierge-cli/shield.svg
   :target: https://pyup.io/repos/github/vshn/concierge-cli
   :alt: Updates
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

**Note:** You need Python >= 3.6, otherwise your installation will not
succeed. (We're doing this really just for Python's awesome f-strings!)
You can use Pipenv to work around this limitation:

.. code-block:: console

    $ pip install pipenv
    $ pipenv shell --three
    $ pip install concierge-cli

Usage Patterns
--------------

#. Manage `project topics`_
#. List projects by topic
#. Manage `group membership`_ and permissions

.. _project topics: https://docs.gitlab.com/ce/user/project/settings/
.. _group membership: https://docs.gitlab.com/ce/user/group/#add-users-to-a-group

Manage topics
^^^^^^^^^^^^^

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

List projects
^^^^^^^^^^^^^

Print a YAML list of all projects matching a topic:

.. code-block:: console

    $ concierge-cli gitlab projects --topic Puppet

Update the list of modules Concierge manages with a specific configuration:

.. code-block:: console

    $ concierge-cli gitlab projects --topic Puppet > configs/foo-bar/managed_modules.yml
    $ git add -v configs/foo-bar/managed_modules.yml
    $ git status && git commit -m 'Added ...' && git push

Group membership
^^^^^^^^^^^^^^^^

**Preparation:** You need an `access token`_ of an administrator user to
list all groups and make changes to any group membership.

.. _access token: https://gitlab.com/profile/personal_access_tokens

List all groups where user is not yet a member of:

.. code-block:: console

    $ concierge-cli gitlab --token *s3cr3t* groups --no-member my.user.name

Add user to all those groups:

.. code-block:: console

    $ concierge-cli gitlab --token *s3cr3t* groups --no-member my.user.name \
                           --set-permission maintainer

List a user's group memberships and permissions:

.. code-block:: console

    $ concierge-cli gitlab --token *s3cr3t* groups my.user.name

Remove a user from selected groups:

.. code-block:: console

    $ concierge-cli gitlab --token *s3cr3t* groups my.user.name \
                           --group-filter a-group-name \
                           --set-permission none
