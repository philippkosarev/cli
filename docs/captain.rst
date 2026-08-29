Captain
=======

Examples
--------

Single-command CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^

``example.py`` file:

.. literalinclude:: singlecommand-example.py
  :language: python

Here is what the user will see when running this CLI:

.. code-block::

  $ ./example.py
  shout: missing argument <TEXT>
  Try 'shout --help' for more information.

  $ ./example.py Hello
  Hello!

  $ ./example.py Hello --world
  Hello world!

  $ ./example.py --help
  Usage:
    shout [OPTION]... <TEXT>
  Description:
    Shouts the given text back.
  Options:
    -w, --world - Adds ' world' before the exclamation mark.
    -h, --help  - Prints this page.


Multi-command CLI
^^^^^^^^^^^^^^^^^^^^^^^^^

``example.py`` file:

.. literalinclude:: multicommand-example.py
  :language: python

Here is what the user will see when running this CLI:

.. code-block::

  $ ./example.py
  very-smart-ai: no command specified.
  Try 'very-smart-ai --help' for more information.

  $ ./example.py shout "I like crisps"
  I like crisps!

  $ ./example.py wonder -h
  Usage:
     very-smart-ai wonder
  Description:
     Where's my copy of My weekend in Stevenage by Filthy Henderson?
  Options:
        --mcbeth - Ponder whether to be or not to be.
     -q --quiet   - Be quiet.
     -h --help    - Prints this page.

  $ ./example.py wonder --mcbeth
  I just want to be a fish.

  $ ./example.py --help
  Trust me, it's the smartest one out there.

  Synopsis:
     very-smart-ai <COMMAND> ...

  Commands:
     shout   - I will be loud!
     whisper - Shhhh! You don't want them to hear you...
     wonder  - Where's my copy of My weekend in Stevenage by Filthy Henderson?

  Usage:
     shout <TEXT> [SUFFIX]
     whisper [LINES]...
     wonder

  Options:
     -h --help - Prints this page.


API
---

.. autoclass:: libjam.Captain

.. autofunction:: libjam.captain
