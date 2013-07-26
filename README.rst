+++++++++++++++++
wikiquote2fortune
+++++++++++++++++

What?
=====

This little script can create a fortune(6) file with quotes from a
Wikiquote_ page; I've tested it only with a few TV Show pages and I
don't know if it will work with movie's quotes.

How?
====

You can install it from source like every other Python package,
running a command like: ::

  # cd /path/to/wikiquote2fortune
  # python setup.py install

Requirements
------------

Since I was in a hurry I've used all the shortcuts available, so you
will need to install a few extra libraries to get the script working:

- BeautifulSoup4
- requests

The `setup.py` file should handle the installation automatically.

This was tested only on Python 2.7, but should also work with 2.6.

Example
-------

To fetch and create a fortune file for Battlestar Galactica: ::

  $ wikiquote2fortune --url 'https://en.wikiquote.org/wiki/Battlestar_Galactica_%282003%29' \
	--output bsg --name 'Battlestar Galactica'
  $ strfile bsg

The command `strfile` is part of the fortune package.

Credits
=======

Daniel Kertesz <daniel@spatof.org>

.. _Wikiquote: https://en.wikiquote.org/wiki/Main_Page
