Aali Flowkit Python documentation |version|
=============================================

The Aali Flowkit Python is a Python service that exposes features from Aali Flowkit to Python users. This documentation provides information on how to install and use the Aali Flowkit Python.

The Aali Flowkit Python offers these main features:



.. grid:: 1 2 2 2


    .. grid-item-card:: Getting started :material-regular:`directions_run`
        :padding: 2 2 2 2
        :link: getting_started/index
        :link-type: doc

        Learn how to install the Aali Flowkit Python in user mode and quickly
        begin using it.

    .. grid-item-card:: User guide :material-regular:`menu_book`
        :padding: 2 2 2 2
        :link: user_guide/index
        :link-type: doc

        Understand key concepts for implementing the Aali Flowkit Python in
        your workflow.

    .. jinja:: main_toctree

        {% if build_api %}
        .. grid-item-card:: API reference :material-regular:`bookmark`
            :padding: 2 2 2 2
            :link: api/src/aali/flowkit/index
            :link-type: doc

            Understand how to use Python to interact programmatically with
            the Aali Flowkit Python.
        {% endif %}

        {% if build_examples %}
        .. grid-item-card:: Examples :material-regular:`play_arrow`
            :padding: 2 2 2 2
            :link: examples/index
            :link-type: doc

            Explore examples that show how to use the Aali Flowkit Python to
            perform many different types of operations.
        {% endif %}

        .. grid-item-card:: Contribute :material-regular:`group`
            :padding: 2 2 2 2
            :link: contributing
            :link-type: doc

            Learn how to contribute to the Aali Flowkit Python codebase or documentation.


.. jinja:: main_toctree

    .. toctree::
       :hidden:
       :maxdepth: 3

       getting_started/index
       user_guide/index
       {% if build_api %}
       api/index
       {% endif %}
       {% if build_examples %}
       examples/index
       {% endif %}
       contributing