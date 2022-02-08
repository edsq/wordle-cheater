import click
from dictionary import letters
from cheater import find_words

@click.command()
def wordle_cheat():
    """Cheat on wordle :(

    Given your current guesses, this utility will print a list of possible solutions.  When entering
    guesses, press space before a letter to mark it as yellow, and tab before a letter to mark it as
    green.
    """

    click.secho('Wordle Cheater :(', bold=True)
    click.echo('Enter current guesses below.')
    click.secho('Mark as yellow: press spacebar', dim=True)
    click.secho('Mark as green:  press esc or tab', dim=True)
    click.echo('\n')
    click.echo('\033[F', nl=False) # Go to the beginning of the last line, leaving space at bottom
    click.echo('    _____\b\b\b\b\b', nl=False)

    guesses = []
    char_index = 0
    entering_guesses = True
    while entering_guesses:
        c = click.getchar()

        if char_index == 5 and c == '\r':
            # We've entered a full word and want a new line (pressed return)
            char_index = 0
            click.echo('\n')
            click.echo('\033[F', nl=False)
            click.echo('    _____\b\b\b\b\b', nl=False)

        elif c == '\x7f' and char_index > 0:
            # Backspace pressed - ignore this if we're at the beginning of the line already
            click.echo('\b_\b', nl=False)
            guesses.pop()
            char_index -= 1

        elif char_index == 5:
            # Only return and delete do anything if we've typed 5 characters already
            continue

        elif char_index == 0 and c == '\r':
            # We've hit return on an empty line and want to exit
            click.echo('     ') # clear last line of underscores
            entering_guesses = False

        elif c == '\x1b' or c == '\t':
            # We want to enter a green colored character
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

    possible_words = find_words(blacks=blacks, yellows=yellows, greens=greens)
    click.echo('Possible words:')
    click.echo(possible_words)


if __name__ == '__main__':
    wordle_cheat()

