Installation
============

Requirements
------------

SchemaScribe requires Python 3.12 or newer.

Install
-------

Install the package, or use an editable install so that changes in ``src/`` take effect immediately:

.. code-block:: bash

   pip install .        # regular install
   pip install -e .     # editable install

Extras
------

Optional dependencies are available as extras:

* ``dev``: development tools (tox, pre-commit, ruff, mypy, pytest, pytest-cov, pytest-custom-exit-code). See :doc:`development` for the workflow.
* ``docs``: documentation dependencies (Sphinx, Furo, sphinx-autodoc-typehints).

.. code-block:: bash

   pip install -e ".[dev]"        # development tools
   pip install -e ".[docs]"       # documentation dependencies
   pip install -e ".[dev,docs]"   # both

Build the documentation locally:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html

Verify
------

Check that the package is installed and that the version is correct:

.. code-block:: bash

  pip show schema-scribe