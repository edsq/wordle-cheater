# wordle-cheater

[![PyPI](https://img.shields.io/pypi/v/wordle-cheater.svg)](https://pypi.org/project/wordle-cheater/)
[![Documentation Status](https://readthedocs.org/projects/wordle-cheater/badge/?version=latest)](https://wordle-cheater.readthedocs.io/en/latest/?badge=latest)
[![Tests](https://github.com/edsq/wordle-cheater/workflows/Tests/badge.svg)](https://github.com/edsq/wordle-cheater/actions?workflow=Tests)
[![codecov](https://codecov.io/gh/edsq/wordle-cheater/branch/main/graph/badge.svg?token=5G6XN19YDV)](https://codecov.io/gh/edsq/wordle-cheater)

![interactive-screenshot](https://github.com/edsq/wordle-cheater/raw/main/docs/_static/wordle-cheater_interactive.png)

Utitlities for cheating on Wordle :(

I created `wordle-cheater` because I often like to do a post-mortem on the day's Wordle
and see how the possible solutions changed with my guesses.  If you use this to
actually cheat on Wordle, you go straight to the naughty list.

[Read the documentation here.](https://wordle-cheater.readthedocs.io/en/latest/)

## Installation

Install with pip or [pipx](https://pypa.github.io/pipx/):
```console
$ pipx install wordle-cheater
```

Requires Python >=3.7, <4.0.

## Usage

Invoked without arguments, `wordle-cheater` allows you to interactively enter your
guesses.  Alternatively, you can specify your guesses on the command line like so:

![cli-screenshot](https://github.com/edsq/wordle-cheater/raw/main/docs/_static/wordle-cheater_cli.png)

Note that we use "b" (for "black") for letters that don't appear in the solution - not
"w" for "white".  Throughout this project, we assume you are using dark mode.

See
```console
$ wordle-cheater --help
```
for more information and options.
