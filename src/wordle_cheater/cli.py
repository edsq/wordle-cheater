import curses
import click
from wordle_cheater.interface import CursesInterface, ClickInterface
from wordle_cheater.interface_base import format_words
from wordle_cheater.cheater import cheat, get_wordle_letters


@click.command()
@click.argument("letters", default="")
@click.argument("colors", default="")
@click.option(
    "--print/--no-print",
    "-p",
    "print_",
    default=False,
    show_default=True,
    help="When interactively entering guesses, print guesses and solutions on exit.",
)
@click.option(
    "--rows",
    default=10,
    show_default=True,
    help="Maximum number of rows to print when '--print' is given.",
)
@click.option(
    "--cols",
    default=8,
    show_default=True,
    help="Number of columns to print when '--print' is given.",
)
@click.option(
    "--use-curses/--no-curses",
    default=True,
    show_default=True,
    help="Use the Curses library for interactive input and output.",
)
def wordle_cheat(letters, colors, print_, use_curses, rows, cols):
    """Cheat on wordle :(

    Given your current guesses (LETTERS) and their colors (COLORS), this utility prints
    a list of possible solutions in random order.  If either LETTERS or COLORS are not
    provided, wordle-cheater has you interactively enter your guesses.

    COLORS must be a string of 'b', 'y', or 'g' characters, corresponding to black,
    yellow, and green, respectively.

    LETTERS and COLORS both ignore whitespace.

    When interactively entering previous guesses, press space once before a letter to
    mark it as yellow, or press space twice to mark it as green.

    Note that no-curses mode is poorly supported and may not work on your terminal.
    """
    # If letters & colors were already given, no need to spawn a UI
    if letters != "" and colors != "":
        guesses = get_wordle_letters(letters, colors)
        possible_words = cheat(guesses)
        out_str = format_words(possible_words, max_rows=rows, max_cols=cols)
        print_ = True

    elif use_curses:
        ui = CursesInterface.init_and_run()
        guesses = ui.guesses
        out_str = ui.get_results_string(max_rows=rows, max_cols=cols)

    else:
        ui = ClickInterface(max_rows=rows, max_cols=cols)
        ui.main()

    # Now print the entered guesses and results, if requested
    # If we're in no-curses mode, don't bother (as they've already been printed)
    if print_ and use_curses:
        click.secho("Wordle Cheater :(", bold=True)
        click.echo()  # Get a new line
        click.echo("    ", nl=False)  # Indent by four spaces
        for wl in guesses:
            if wl.color == "black":
                # Have to treat black differently since the fg needs to be white
                click.secho(wl.letter.upper(), fg="white", bg="black", nl=False)

            else:
                click.secho(wl.letter.upper(), fg="black", bg=wl.color, nl=False)

            # If we're at the end of the word (5 letters), go to the next line
            if wl.index == 4:
                click.echo()  # Get a new line
                click.echo("    ", nl=False)  # Indent by four spaces

        click.echo()
        click.secho("Possible solutions:", underline=True)
        click.secho(out_str)


if __name__ == "__main__":
    wordle_cheat()
