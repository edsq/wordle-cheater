import click
from wordle_cheater.dictionary import letters
from wordle_cheater.cheater import find_words


def move_cursor_down_left(n):
    """Move cursor down n lines and to beginning of line."""
    click.echo(f"\033[{n}E", nl=False)


def move_cursor_up_left(n):
    """Move cursor up n lines and to beginning of line."""
    click.echo(f"\033[{n}F", nl=False)


def hide_cursor():
    """Hide the cursor."""
    click.echo("\033[?25l", nl=False)


def show_cursor():
    """Show the cursor."""
    click.echo("\033[?25h", nl=False)


def clear_line():
    """Clear current line and return cursor to left."""
    click.echo("\033[2K\r", nl=False)


@click.command()
@click.option(
    "--rows", default=10, show_default=True, help="Maximum number of rows to print"
)
@click.option(
    "--cols", default=8, show_default=True, help="Number of columns to print."
)
def wordle_cheat(rows, cols):
    """Cheat on wordle :(

    Given your current guesses, this utility will print a list of possible solutions.  When entering
    guesses, press space before a letter to mark it as yellow, and esc or tab before a letter to
    mark it as green.
    """

    click.secho("Wordle Cheater :(", bold=True)
    click.echo("Enter guesses below.")
    click.secho("Mark as yellow: spacebar", dim=True)
    click.secho("Mark as green:  esc or tab", dim=True)
    click.echo("")

    guesses = get_guesses()
    get_results(guesses, rows=rows, cols=cols)


def get_guesses():
    click.echo("")  # Add empty line below cursor
    move_cursor_up_left(1)
    click.echo("    _____\b\b\b\b\b", nl=False)  # First line of underscores

    guesses = []
    char_index = 0
    entering_guesses = True
    while entering_guesses:
        c = click.getchar()

        if c == "\r":
            # Return pressed
            if len(guesses) == 30 and char_index == 5:
                # We've used all 6 guesses
                click.echo("\n")
                entering_guesses = False

            elif char_index == 0:
                # We've hit return on an empty line and want to exit
                clear_line()  # Clear line of underscores
                click.echo("")  # End with blank line
                entering_guesses = False

            elif char_index == 5:
                # We've entered a full word and want a new line (pressed return)
                char_index = 0
                click.echo("\n")  # Leave a blank line below cursor
                move_cursor_up_left(1)
                click.echo("    _____\b\b\b\b\b", nl=False)

        elif c == "\x7f" and char_index > 0:
            # Backspace pressed - ignore this if we're at the beginning of the line already
            click.echo("\b_\b", nl=False)
            guesses.pop()
            char_index -= 1

        elif char_index == 5:
            # Only return and delete do anything if we've typed 5 characters already
            continue

        elif c == "\x1b" or c == "\t":
            # Escape or tab pressed - we want to enter a green colored character
            hide_cursor()
            click.secho(
                "_\b", bg="green", fg="black", nl=False
            )  # show colored underscore

            c = click.getchar()
            if c.upper() not in letters:
                show_cursor()
                click.echo("_\b", nl=False)  # uncolor underscore
                continue

            click.secho(c.upper(), bg="green", fg="black", nl=False)
            show_cursor()

            guesses.append(("g", char_index, c.lower()))
            char_index += 1

        elif c == " ":
            # Space pressed - we want to enter a yellow colored character
            hide_cursor()
            click.secho(
                "_\b", bg="yellow", fg="black", nl=False
            )  # show colored underscore

            c = click.getchar()
            if c.upper() not in letters:
                show_cursor()
                click.echo("_\b", nl=False)  # uncolor underscore
                continue

            click.secho(c.upper(), bg="yellow", fg="black", nl=False)
            show_cursor()

            guesses.append(("y", char_index, c.lower()))
            char_index += 1

        elif c.upper() in letters:
            # We want to enter a "black" colored character
            click.secho(c.upper(), nl=False, bg="black", fg="white")

            guesses.append(("b", char_index, c.lower()))
            char_index += 1

    return guesses


def get_results(guesses, rows=4, cols=4):
    """Get possible words given `guesses` and print them nicely.

    Positional arguments
    --------------------
    guesses : list of tuples
        The previously guessed results.  Each tuple should be of the form
        `(color, index, letter)` where `color` is one of 'b', 'y', 'g' (referring to the marked
        color of `letter`: 'black', 'yellow', or 'green', respectively), `index` is the letter's
        position in the word (indexing from 0), and `letter` is the letter in question.

    Keyword arguments
    -----------------
    rows : int
        The maximum number of rows to print before using a pager.
    cols : int
        The number of columns to print of results.
    """

    blacks = []
    yellows = [[], [], [], [], []]
    greens = [None, None, None, None, None]

    # Get black characters first so we can check against them
    for color, index, char in guesses:
        if color == "b":
            blacks.append(char)

    for color, index, char in guesses:
        if color == "y":
            if char in blacks:
                raise ValueError(f"{char} appears as both black and yellow")

            yellows[index].append(char)

        elif color == "g":
            if char in blacks:
                raise ValueError(f"{char} appears as both black and green")

            if greens[index] is not None and greens[index] != char:
                raise ValueError(
                    f"{greens[index]} and {char} are both marked green in the same location"
                )

            greens[index] = char

    # Get list of possible words
    possible_words = find_words(blacks=blacks, yellows=yellows, greens=greens)

    # Format output
    lines = [
        "\t".join(possible_words[i : i + cols])
        for i in range(0, len(possible_words), cols)
    ]

    if len(lines) > rows:
        # Truncate some rows
        out_str = "\n".join(lines[0:rows])
        n_missing = int(len(possible_words) - rows * cols)
        out_str += f"\n...({n_missing} more)"

    else:
        out_str = "\n".join(lines)

    click.secho("Possible solutions:", underline=True)
    click.echo(out_str)


if __name__ == "__main__":
    wordle_cheat()
