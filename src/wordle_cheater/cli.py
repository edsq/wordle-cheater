"""Command-line interface for wordle-cheater."""
import click
from wordle_cheater.cheater import cheat, get_wordle_letters
from wordle_cheater.interface import ClickInterface, CursesInterface
from wordle_cheater.interface_base import format_words


@click.command()
@click.argument("words", default="")
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
    help="Maximum rows of possible solutions to print.",
)
@click.option(
    "--cols",
    default=8,
    show_default=True,
    help="Maximum columns of possible solutions to print.",
)
@click.option(
    "--simple-print/--no-simple-print",
    default=False,
    show_default=True,
    help="Print all solutions, separated by a space.  Useful for machine-parsing.",
)
@click.option(
    "--use-curses/--no-curses",
    default=True,
    show_default=True,
    help="Use the Curses library for interactive input and output.",
)
def wordle_cheat(words, colors, print_, rows, cols, simple_print, use_curses):
    """Cheat on Wordle :(

    Given your current guesses (WORDS) and their colors (COLORS), this utility prints
    a list of possible solutions in random order.  If either WORDS or COLORS are not
    provided, wordle-cheater has you interactively enter your guesses.

    COLORS must be a string of 'b', 'y', or 'g' characters, corresponding to black,
    yellow, and green, respectively.

    WORDS and COLORS both ignore whitespace.

    When interactively entering guesses, press space once before a letter to mark it as
    yellow, or press space twice to mark it as green.

    Note that no-curses mode is poorly supported and may not work on your terminal.

    """  # noqa: D400 DAR101
    # If words & colors were already given, no need to spawn a UI
    if words != "" and colors != "":
        guesses = get_wordle_letters(words, colors)
        print_ = True  # Ensure we print results

    elif use_curses:  # pragma: no cover
        ui = CursesInterface.init_and_run()
        guesses = ui.guesses

    else:  # pragma: no cover
        ui = ClickInterface(max_rows=rows, max_cols=cols)
        ui.main()
        return  # ClickInterface prints solutions automatically, so we're done

    # Get possible words
    possible_words = cheat(guesses)

    # Now print the entered guesses and results, if requested
    if simple_print:
        out_str = " ".join(possible_words)
        click.echo(out_str)

    elif print_:
        out_str = format_words(possible_words, max_rows=rows, max_cols=cols)
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

    else:  # pragma: no cover
        return


if __name__ == "__main__":
    wordle_cheat()  # pragma: no cover
