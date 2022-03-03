import curses
import click
from wordle_cheater.interface import CursesInterface, ClickInterface


@click.command()
@click.option(
    "--print/--no-print",
    "-p",
    "print_",
    default=False,
    show_default=True,
    help="Print guesses and solutions to stdout.",
)
@click.option(
    "--rows",
    default=10,
    show_default=True,
    help="Maximum number of rows to print when printing output.",
)
@click.option(
    "--cols",
    default=8,
    show_default=True,
    help="Number of columns to print when printing output.",
)
@click.option(
    "--use-curses/--no-curses",
    default=True,
    show_default=True,
    help="Use the Curses library for input and output.",
)
def wordle_cheat(print_, use_curses, rows, cols):
    """Cheat on wordle :(

    Given your current guesses, this utility will print a list of possible solutions
    (in no particular order).  When entering previous guesses, press space once before
    a letter to mark it as yellow, or press space twice to mark it as green.

    Note that no-curses mode is poorly supported and may not work on your terminal.
    """
    if use_curses:
        ui = CursesInterface.init_and_run()
    else:
        ui = ClickInterface(max_rows=rows, max_cols=cols)
        ui.main()

    # Now print the entered guesses and results, if requested
    # If we're in no-curses mode, don't bother (as they've already been printed)
    if print_ and use_curses:
        out_str = ui.get_results_string(max_rows=rows, cols=cols)

        click.secho("Wordle Cheater :(", bold=True)
        click.echo()  # Get a new line
        click.echo("    ", nl=False)  # Indent by four spaces
        for wl in ui.guesses:
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
