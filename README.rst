+++++++++++++++++
wikiquote2fortune
+++++++++++++++++

What?
=====

This little Python 3 script can create a fortune(6) file with quotes from a Wikiquote_ page; I've
only tested it on a few TV Show pages and the parser is not very robust.

How?
====

You can install it from source like every other Python package, running a command like: ::

  # cd /path/to/wikiquote2fortune
  # python setup.py install

You can also use Poetry_: ::

  $ cd wikiquote2fortune
  $ poetry install
  $ poetry run wikiquote2fortune --help

Example
-------

To fetch and create a fortune file for Star Trek TNG: ::

  $ wikiquote2fortune -o star_trek_TNG Star_Trek:_The_Next_Generation
  $ strfile star_trek_TNG

NOTE: the command `strfile` is part of the fortune package.

Credits
=======

Daniel Kertesz <daniel@spatof.org>

.. _Wikiquote: https://en.wikiquote.org/wiki/Main_Page
.. _Poetry: https://github.com/sdispater/poetry
