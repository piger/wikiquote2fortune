# wikiquote2fortune

## What?

This little Python script can create a fortune(6) file with quotes from a
[Wikiquote](https://en.wikiquote.org/wiki/Main_Page) page; I've only
tested it on a few TV Show pages and the parser is not very robust.

## How?

You can install it from source like every other Python package, running a command like:

```
$ python3 -m venv ./venv
$ . ./venv/bin/activate
$ python3 setup.py install
```

## Example

To fetch and create a fortune file for Star Trek TNG:

```
$ wikiquote2fortune -o star_trek_TNG Star_Trek:_The_Next_Generation
$ strfile star_trek_TNG
```

NOTE: the command `strfile` is part of the fortune package.
