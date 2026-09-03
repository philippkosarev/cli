https://github.com/philippkosarev/cli

CLI
===

Python library for writing command line **interfaces**, *not parsers*.

Installation
------------

To install the in-development version:

.. code-block::

  pip install git+https://github.com/philippkosarev/cli.git


.. note:: Stable releases should be coming soon.


Examples
--------

Single-command CLI
^^^^^^^^^^^^^^^^^^

``shout.py`` file:

.. literalinclude:: shout.py
  :language: python

Here is what the user will see when running this CLI:

.. command-output:: ./shout.py
  :returncode: 64

.. command-output:: ./shout.py Hello

.. command-output:: ./shout.py Hello --world

.. command-output:: ./shout.py --help


Multi-command CLI
^^^^^^^^^^^^^^^^^

``multi.py`` file:

.. literalinclude:: multi.py
  :language: python

Here is what the user will see when running this CLI:

.. command-output:: ./multi.py
  :returncode: 64

.. command-output:: ./multi.py shout "I like crisps"

.. command-output:: ./multi.py wonder -h

.. command-output:: ./multi.py wonder --mcbeth

.. command-output:: ./multi.py --help


API
---

.. autoclass:: cli.CLI

.. autofunction:: cli.__call__

.. autoclass:: cli.Option

.. autoclass:: cli.Partial

.. autofunction:: cli.part
