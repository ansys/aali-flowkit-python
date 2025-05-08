.. _ref_getting_started:

Getting started
###############

This section describes how to install the Allie Flowkit Python in user mode and
quickly begin using it. If you are interested in contributing to the Allie Flowkit Python,
see :ref:`contribute` for information on installing in developer mode.

Installation
============

To use `pip <https://pypi.org/project/pip/>`_ to install the Allie Flowkit Python,
run this command:

.. code:: bash

        pip install allie-flowkit-python

Alternatively, to install the latest version from this library's
`GitHub repository <https://github.com/ansys/allie-flowkit-python/>`_,
run these commands:

.. code:: bash

    git clone https://github.com/ansys/allie-flowkit-python
    cd allie-flowkit-python
    pip install .

Quick start
^^^^^^^^^^^

The following examples show how to use the Allie Flowkit Python.

.. code:: bash

    allie-flowkit-python --host 0.0.0.0 --port 50052 --workers 1


