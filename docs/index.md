# wordle-cheater

[![Tests](https://github.com/edsq/wordle-cheater/workflows/Tests/badge.svg)](https://github.com/edsq/wordle-cheater/actions?workflow=Tests)
[![codecov](https://codecov.io/gh/edsq/wordle-cheater/branch/main/graph/badge.svg?token=5G6XN19YDV)](https://codecov.io/gh/edsq/wordle-cheater)

```{toctree}
:hidden:
:maxdepth: 2

cli_reference
reference
license
```

![interactive-screenshot](_static/wordle-cheater_interactive.png)

Utitlities for cheating on Wordle :(

I created `wordle-cheater` because I often like to do a post-mortem on the day's Wordle
and see how the possible solutions changed with my guesses.  If you use this to
actually cheat on Wordle, you go straight to the naughty list.


## Installation

Install with pip or [pipx](https://pypa.github.io/pipx/):
```console
$ pipx install wordle-cheater
```

Requires Python >=3.7, <4.0.

## Usage

Invoked without arguments, `wordle-cheater` allows you to interactively enter your
guesses.  Alternatively, you can specify your guesses on the command line like so:

![cli-screenshot](_static/wordle-cheater_cli.png)

Note that we use "b" (for "black") for letters that don't appear in the solution - not
"w" for "white".  Throughout this project, we assume you are using dark mode.

See
```console
$ wordle-cheater --help
```
or the [command-line reference](cli_reference.md) for more information and options.
