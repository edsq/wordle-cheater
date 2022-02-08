import click
from wordle_cheater.dictionary import letters
from wordle_cheater.cheater import find_words

@click.command()
@click.option('--rows', default=10, show_default=True, help='Maximum number of rows to print')
@click.option('--cols', default=8, show_default=True, help='Number of columns to print.')
def wordle_cheat(rows, cols):
    """Cheat on wordle :(

    Given your current guesses, this utility will print a list of possible solutions.  When entering
    guesses, press space before a letter to mark it as yellow, and esc or tab before a letter to
    mark it as green.
    """

    click.secho('Wordle Cheater :(', bold=True)
    click.echo('Enter guesses below.')
    click.secho('Mark as yellow: spacebar', dim=True)
    click.secho('Mark as green:  esc or tab', dim=True)
    click.echo('\n\n\033[F', nl=False)
    click.echo('    _____\b\b\b\b\b', nl=False)

    guesses = []
    char_index = 0
    entering_guesses = True
    while entering_guesses:
        c = click.getchar()

        if c == '\r':
            if len(guesses) == 30 and char_index == 5:
                # We've used all 6 guesses
                click.echo('\n')
                entering_guesses = False

            elif char_index == 0:
                # We've hit return on an empty line and want to exit
                click.echo('\033[2K\r') # Clear line of underscores
                entering_guesses = False

            elif char_index == 5:
                # We've entered a full word and want a new line (pressed return)
                char_index = 0
                click.echo('\n\n\033[F', nl=False) # Leave a blank line below cursor
                click.echo('    _____\b\b\b\b\b', nl=False)

        elif c == '\x7f' and char_index > 0:
            # Backspace pressed - ignore this if we're at the beginning of the line already
            click.echo('\b_\b', nl=False)
            guesses.pop()
            char_index -= 1

        elif char_index == 5:
            # Only return and delete do anything if we've typed 5 characters already
            continue

        elif c == '\x1b' or c == '\t':
            # We want to enter a green colored character if user presses escape or tab
            c = click.getchar()
            if c.upper() not in letters:
                continue

            click.secho(c.upper(), bg='green', fg='black', nl=False)

            guesses.append(('g', char_index, c.lower()))
            char_index += 1

        elif c == ' ':
            # We want to enter a yellow colored character
            c = click.getchar()
            if c.upper() not in letters:
                continue

            click.secho(c.upper(), bg='yellow', fg='black', nl=False)

            guesses.append(('y', char_index, c.lower()))
            char_index += 1

        elif c.upper() in letters:
            # We want to enter a "black" colored character
            click.secho(c.upper(), nl=False, bg='black', fg='white')

            guesses.append(('b', char_index, c.lower()))
            char_index += 1

    get_results(guesses, rows=rows, cols=cols)


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
        if color == 'b':
            blacks.append(char)

    for color, index, char in guesses:
        if color == 'y':
            if char in blacks:
                raise ValueError(f'{char} appears as both black and yellow')

            yellows[index].append(char)

        elif color == 'g':
            if char in blacks:
                raise ValueError(f'{char} appears as both black and green')

            if greens[index] is not None and greens[index] != char:
                raise ValueError(f'{greens[index]} and {char} are both marked green in the same location')
            
            greens[index] = char

    # Get list of possible words
    possible_words = find_words(blacks=blacks, yellows=yellows, greens=greens)

    # Format output
    lines = ['\t'.join(possible_words[i:i+cols]) for i in range(0, len(possible_words), cols)]
    out_str = '\n'.join(lines)

    if len(lines) > rows:
        long_out_str = click.style('Possible solutions:', underline=True) + '\n'
        long_out_str += out_str
        click.echo_via_pager(long_out_str)

    else:
        click.secho('Possible solutions:', underline=True)
        click.echo(out_str)


if __name__ == '__main__':
    wordle_cheat()

