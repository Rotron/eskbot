eskbot
======


Introduction
============
``eskbot``'s full name is Eskarina Smith. Their knowledge set comes from `A.L.I.C.E.`_.

They are powered by `Twisted's`_ `IRCClient`_


Example Use
============
Doing this in a `virtualenv`_ is highly recommended.


.. code-block:: pycon

    $ git clone https://github.com/ashfall/eskbot
    $ cd eskbot
    $ pip install .
    $ cd eskbot
    $ python eskbot.py irc.freenode.net 6667 twisted-bots

Or alternately, replace ``irc.freenode.net`` and ``twisted-bots`` with your
desired IRC server and channel.

Once connected, eskbot will respond to:
    - any message sent privately, e.g. ``/msg eskarina Hi!``, or
    - any message addressed directly to them, i.e. prefixed with their name and
      a ``:``. e.g. ``eskarina: Hi!``


.. _`A.L.I.C.E.`: http://www.alicebot.org/downloads/sets.html
.. _`Twisted's`: https://twistedmatrix.com/
.. _`IRCClient`: http://twistedmatrix.com/documents/current/api/twisted.words.protocols.irc.IRCClient.html
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/userguide/#usage
