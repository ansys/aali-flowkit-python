.. _contribute:

Contribute
##########

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_ topic
in the *PyAnsys developer's guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to the Allie Flowkit Python.

The following contribution information is specific to the Allie Flowkit Python.


Clone the repository
--------------------

To clone and install the latest *Allie Flowkit Python* release in development mode, run
these commands:

.. code::

    git clone https://github.com/ansys/allie-flowkit-python/
    cd allie-flowkit-python
    python -m pip install --upgrade pip
    pip install -e .

Adhere to code style
--------------------

*Allie Flowkit Python* follows the PEP8 standard as outlined in PEP 8 in the PyAnsys Developer’s Guide and implements style checking using pre-commit.

To ensure your code meets minimum code styling standards, run these commands:

.. code::

    pip install pre-commit
    pre-commit run --all-files

You can also install this as a pre-commit hook by running this command:

.. code::

    pre-commit install

Run the tests
-------------

Prior to running the tests, you must run this command to install the test dependencies:

.. code::

    pip install -e .[tests]

To run the tests, navigate to the root directory of the repository and run this command:

.. code::

    pytest

Build the documentation
-----------------------

Prior to building the documentation, you must run this command to install the documentation dependencies:

.. code::

    pip install -e .[doc]

To build the documentation, run the following commands:

.. code::

    cd doc

    # On linux
    make html

    # On windows
    ./make.bat html

The documentation is built in the `docs/_build/html` directory.
