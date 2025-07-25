.. _ref_getting_started:

Getting started
###############

This section describes how to install the Aali Flowkit Python in user mode and
quickly begin using it. If you are interested in contributing to the Aali Flowkit Python,
see :ref:`contribute` for information on installing in developer mode.

Installation
============

To use `pip <https://pypi.org/project/pip/>`_ to install the Aali Flowkit Python,
run this command:

.. code:: bash

        pip install aali-flowkit-python

Alternatively, to install the latest version from this library's
`GitHub repository <https://github.com/ansys/aali-flowkit-python/>`_,
run these commands:

.. code:: bash

    git clone https://github.com/ansys/aali-flowkit-python
    cd aali-flowkit-python
    pip install .

Quick start
^^^^^^^^^^^

The following examples show how to use the Aali Flowkit Python.

.. code:: bash

    aali-flowkit-python --host 0.0.0.0 --port 50052 --workers 1


