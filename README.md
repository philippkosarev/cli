# CLI
Python library for writing command line __interfaces__, _not parsers_.

## Motivation
The traditional way of creating command line interfaces in Python involves initialising a parser, then writing a hundred lines of boilerplate code that configures it and then writing another 50 lines of code which manually passes the parsed arguments to functions. Libraries like [`click`](https://github.com/pallets/click) lighten the amount of the boilerplate in comparision to the traditional [`argparse`](https://docs.python.org/3/library/argparse.html), it might get us down to about 30-40 lines of boilerplate, while also introducing some new issues. For a lot of programs, this is not enough of an advantage to forgo using the traditional standard of [`argparse`](https://docs.python.org/3/library/argparse.html).

This library aims to forgo the boilerplate entirely, instead using Python's great introspection features to allow creation of portable, quick and intuitive command line __interfaces__.

## Installation
To install the in-development version:
```sh
pip install git+https://github.com/philippkosarev/cli.git
```

> [!NOTE]
> Stable releases should be coming soon.


## Documentation
The documentation, with examples, is available [here](https://philippkosarev.github.io/cli).
