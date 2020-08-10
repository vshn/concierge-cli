Contributing
============

You can contribute to this project by opening a ticket or a pull request.
Feel free to ask for clarification or help by creating a ticket before you
start with a pull request!

Development environment
-----------------------

You only need Python 3 standard tools, including `tox`, for contributing code
and running linting and tests.

If you want to run the `concierge-cli` locally install the dependencies, e.g.

```console
python3 -m pip install -r requirements.txt
```

or, if you use Pipenv:

```console
pipenv install --dev
```

Running tests
-------------

When you make changes to the code you should always include tests that cover
your changes. Run the linters and our test suite using Tox, e.g.

```console
# show all Tox targets
tox -lv
```
```console
# run just flake8 and the test for Python 3.7
tox -e flake8,py37
```
```console
# update dependencies (generate requirements.txt)
tox -e requirements
```
```console
# run entire test suite
tox
```

The entire suite will run on Travis when you create a PR.
Make sure all tests pass, otherwise the PR will likely not get merged.

Developing locally
------------------

You can try out the CLI by running the application as a module, e.g.

```console
python3 -m concierge_cli
```

or you can make a so-called "editable install", for development:

```console
python3 setup.py develop
# or:
python3 -m pip install -e .
```

Then run as usual:

```console
concierge-cli --help
```

Install from repository
-----------------------

If you only want to install `concierge-cli` off the Git repository, e.g.
in order to try out a feature branch, you can install it on your machine
like this:

```console
python3 -m pip install git+https://github.com/vshn/concierge-cli#egg=concierge-cli
```

Or, for a specific branch:

```console
python3 -m pip install git+https://github.com/vshn/concierge-cli@feature-branch#egg=concierge-cli
```
