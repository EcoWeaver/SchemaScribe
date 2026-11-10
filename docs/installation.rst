Installation
============

Requirements
------------

* Python 3.12 or newer

Install
-------

.. code-block:: bash

   pip install .

Editable install
----------------

.. code-block:: bash

   pip install -e .

Development
-----------

.. code-block:: bash

   pip install -e ".[dev]"

Documentation
-------------

Install the documentation dependencies:

.. code-block:: bash

   pip install -e ".[docs]"

Build the documentation locally:

.. code-block:: bash

   sphinx-build -b html docs docs/_build/html