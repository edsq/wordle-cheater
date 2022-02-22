import curses
import click
from wordle_cheater.interface import CursesInterface, ClickInterface


@click.command()
@click.option(
    "--use-curses/--no-curses",
    default=True,
    show_default=True,
    help="Whether or not to use the Curses library for input and output.",
)
@click.option(
    "--rows",
    default=10,
    show_default=True,
    help="Maximum number of rows to print in no-curses mode.",
)
@click.option(
    "--cols",
    default=8,
    show_default=True,
    help="Number of columns to print in no-curses mode.",
)
def wordle_cheat(use_curses, rows, cols):
    """Cheat on wordle :(

    Given your current guesses, this utility will print a list of possible solutions
    (in no particular order).  When entering previous guesses, press space once before
    a letter to mark it as yellow, or press space twice to mark it as green.

    Note that no-curses mode is poorly supported and may not work on your terminal.
    """
    if use_curses:
        ui = CursesInterface()
        curses.wrapper(ui.main)
    else:
        ui = ClickInterface(max_rows=rows, max_cols=cols)
        ui.main()


if __name__ == "__main__":
    wordle_cheat()
