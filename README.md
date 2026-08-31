# CLI
Python library for writing command line __interfaces__, _not parsers_.

## Documentation
The documentation, with examples, is available [here](https://philippkosarev.github.io/cli).

## Motivation
The traditional way of creating command line interfaces in Python involves initialising a parser, then writing a hundred lines of boilerplate code that configures it and then writing another 50 lines of code which manually passes the parsed arguments to functions. Libraries like [`click`](https://github.com/pallets/click) lighten the amount of the boilerplate in comparision to the traditional [`argparse`](https://docs.python.org/3/library/argparse), it might get us down to about 30-40 lines of boilerplate, while also introducing some new issues. For a lot of programs, this is not enough of an advantage to forgo using the traditional standard of [`argparse`](https://docs.python.org/3/library/argparse).

This library aims to forgo the boilerplate entirely, instead using Python's great introspection features to allow creation of portable, quick and intuitive command line __interfaces__.

## Quickstart
### Installation
To install the in-development version:
```sh
pip install git+https://github.com/philippkosarev/cli.git
```
> [!NOTE]
> Stable releases should be coming soon.

### First CLI
Let's say we want to create a CLI around a function called `shout` which echoes the given input and appends a `!` to the end:
```py
def shout(text):
  print(text + '!')
```

To create a CLI around this `shout` function with [`argparse`](https://docs.python.org/3/library/argparse), you would have to write something like this:
```py
from argparse import ArgumentParser

def shout(text):
  print(text + '!')

parser = ArgumentParser()
parser.add_argument('text')
parsed = parser.parse_args()
shout(parsed.text)
```

<details><summary>Help page from this CLI</summary>

```
$ ./shout.py --help
usage: shout.py [-h] text

positional arguments:
  text

options:
  -h, --help  show this help message and exit
```

</details>

You can see that this involves creating an instance of `ArgumentParser` (which is not connected to our `shout` function), manually adding the `text` argument, parsing the arguments and manually passing the `text` argument to our `shout` function.

Now here is the same CLI, but made with this library:
```py
import cli

def shout(text):
  print(text + '!')

shout_cli = cli(main)
shout_cli()
```

<details><summary>Help page from this CLI</summary>

```
./shout.py --help
Usage:
   shout.py [OPTIONS]... <TEXT>
Options:
   -h, --help - Prints this page.
```

</details>

The created `shout_cli` directly took the `shout` function as its target, saw that it requires a parameter called `text` and then, upon running, automatically passed it to `shout`.

You can find more examples and explanations in the [documentation](https://philippkosarev.github.io/cli).
