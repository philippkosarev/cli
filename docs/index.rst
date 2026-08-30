https://github.com/philippkosarev/cli

CLI
===

Python library for writing command **interfaces**, *not parsers*.

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

.. code-block::

  $ ./shout.py
  shout.py: missing arguments <TEXT>
  Try 'shout.py --help' for more information.

  $ ./shout.py Hello
  Hello!

  $ ./shout.py Hello --world
  Hello world!

  $ ./shout.py --help
  Usage:
     shout.py [OPTIONS]... <TEXT>
  Description:
     Shouts the given text back.
  Options:
     -w, --world - Adds " world" before the exclamation mark.
     -h, --help  - Prints this page.



Multi-command CLI
^^^^^^^^^^^^^^^^^

``multi.py`` file:

.. literalinclude:: multi.py
  :language: python

Here is what the user will see when running this CLI:

.. code-block::

  $ ./multi.py
  very-smart-ai: no command specified.
  Try 'very-smart-ai --help' for more information.

  $ ./multi.py shout "I like crisps"
  I like crisps!

  $ ./multi.py wonder -h
  Usage:
     very-smart-ai wonder [OPTIONS]...
  Description:
     Where's my copy of My Weekend in Stevenage by Filthy Henderson?
  Options:
         --mcbeth - Ponder whether to be or not to be.
     -q, --quiet  - Be quiet.
     -h, --help   - Prints this page.

  $ ./multi.py wonder --mcbeth
  I just want to be a fish.

  $ ./multi.py --help
  Trust me, it's the smartest one out there.

  Synopsis:
     very-smart-ai <COMMAND> ...

  Commands:
     shout   - I will be loud!
     whisper - Shhhh! You don't want them to hear you...
     wonder  - Where's my copy of My Weekend in Stevenage by Filthy Henderson?

  Usage:
     shout [OPTIONS]... <TEXT> [SUFFIX]
     whisper [OPTIONS]... [LINES]...
     wonder [OPTIONS]...

  Options:
     -h, --help - Prints this page.


API
---

.. autofunction:: cli.__call__

.. autofunction:: cli.opt

.. autoclass:: cli.CLI

