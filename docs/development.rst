Development
===========

This page describes the development workflow for contributors.

Setup
-----

.. code-block:: bash

   pip install -e ".[dev,docs]"
   pre-commit install

Pre-commit hooks
----------------

``pre-commit`` runs automatically on every ``git commit`` and checks only the staged files. 
Run ``git add`` first: modified but unstaged files and new untracked files are skipped.

Some hooks modify files, in which case the commit is aborted and the files are changed on disk. 
Review the changes, stage them again with ``git add`` and then commit again.

.. code-block:: bash

   pre-commit run              # staged files only
   pre-commit run --all-files  # whole repository

Tox
---

``tox`` runs the CI checks on the whole repository, each in its own isolated environment. 
It is rather slow, so it is not meant to run on every change. 
Use it mainly to run the unit tests in a clean environment and to reproduce a failing CI run locally.

.. code-block:: text

   tox              # lint, type, test
   tox -e lint      # ruff check and format check
   tox -e type      # mypy
   tox -e test      # pytest with coverage

Commit messages
---------------

Commits use one of the following prefixes and reference the issue in the message, for example ``docs: add documentation skeleton, closes #26``.

.. code-block:: text

   feat:      New feature or change to an existing feature
   fix:       Bug fix
   docs:      Documentation
   test:      Add or change tests
   refactor:  Refactoring without behavior change
   ci:        CI/CD configuration
   style:     Formatting (primarily UI)

Continuous integration
----------------------

On every push and pull request, GitHub Actions runs ``tox`` on Ubuntu with Python 3.12. This includes:

* Linting and format check with ruff
* Type checking with mypy
* Tests with pytest and coverage

Documentation
-------------

The documentation is not part of the CI pipeline and is built by Read the Docs on every push (see ``.readthedocs.yaml``). Warnings fail the build, so check locally first:

.. code-block:: bash

   sphinx-build -W -b html docs docs/_build/html