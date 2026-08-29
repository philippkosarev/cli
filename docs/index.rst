https://github.com/philippkosarev/libjam

libjam
======

A jam of Python libraries.


Overview
--------

Here is a quick overview of each module/class in libjam:

- The :doc:`captain` class provides a boilerplate-free way of creating CLIs.
- The :doc:`secretary` class is just another program configuration system.
- The :doc:`writer` module makes it easy to format and style your terminal output.
- The :doc:`flashcard` module has a few functions for getting user input in the terminal.
- The :doc:`drawer` module provides some missing file-management pieces.
- The :doc:`path` class is an extension of ``pathlib.Path`` with :doc:`drawer`'s functionality.


Installing
----------

Releases are available on `PyPi <https://pypi.org/project/libjam/>`_ and can be installed using pip:

.. code-block:: sh

  pip install libjam


Table of contents
-----------------

.. toctree::
  :maxdepth: 2

  captain
  secretary
  writer
  flashcard
  drawer
  path
