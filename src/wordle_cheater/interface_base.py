"""Base class & utilities for interfaces."""
import wordle_cheater.cheater as cheater
from wordle_cheater.dictionary import letters as english_letters


def format_words(words, max_rows=10, max_cols=8, sep="     "):
    """Format a list of strings into columns.

    If `len(words) > max_rows * max_cols`, then the last line of the output string will
    instead indicate how many words are not included.  Note that this line counts
    against the row limit.

    Parameters
    ----------
    words : list of str
        The words to be formatted.
    max_rows : int, optional
        The maximum number of rows to display.  If the full string would require
        more than `max_rows` rows, show an ellipsis and the number of missing
        words on the last line instead.
    max_cols : int, optional
        The number of words per row.
    sep : str, optional
        The character(s) to put in between each column.  Defaults to '     '
        (five spaces) so the space in between each column is the same as the width
        of each column.

    Returns
    -------
    out_str : str
        `words` formatted into a single string of rows and columns.
    """
    lines = [sep.join(words[i : i + max_cols]) for i in range(0, len(words), max_cols)]
    if len(lines) > max_rows:
        lines = lines[: max_rows - 1]
        n_missing = int(len(words) - (max_cols * len(lines)))
        out_str = "\n".join(lines)
        out_str += f"\n...({n_missing} more)"
    else:
        out_str = "\n".join(lines)

    return out_str


class WordleCheaterUI:
    """Base class for handling logic of interface, independent of output method.

    Attributes
    ----------
    guesses : list of WordleLetter objects
        The currently entered guesses.
    entering_letters : bool
        Whether or not we are currently entering guesses.
    """

    def __init__(self):
        self.guesses = []  # List of WordleLetter objects representing current guesses.
        self.entering_letters = False  # Whether or not we're entering previous guesses

    def main(self):
        """Run the interface.

        Main entry point; called by the CLI.
        """
        self.print_title()
        self.enter_letters()
        self.print_results()

    def enter_letters(self, x0=0, y0=0):
        """Enter previous guesses with a wordle-like interface.

        This method both returns and sets `self.guesses`.

        Parameters
        ----------
        x0 : int, optional
            The horizontal position of the upper-left corner of the words to enter.
        y0 : int, optional
            The vertical position of the upper-left corner of the words to enter.

        Returns
        -------
        guesses : list of WordleLetter objects
        """
        x, y = x0, y0  # Location of cursor.  (0, 0) is top left corner.
        self.print(x, y, "_____")  # Start with a blank line of underscores
        self.move_cursor(x, y)
        self.guesses = []
        self.entering_letters = True
        while self.entering_letters:
            # Get keypress
            c = self.get_key()

            # Check if user pressed return
            if self.is_enter(c):
                # Check if we've entered all 6 words
                if y == y0 + 5 and x == x0 + 5:
                    self.entering_letters = False  # Exit loop

                # Check if user pressed return on an empty line and wants to exit
                elif x == x0:
                    self.set_cursor_visibility(False)  # Hide cursor
                    self.print(x, y, "     ")  # Clear line of underscores
                    self.entering_letters = False  # Exit loop

                # Check if user pressed return on a full line and wants another
                elif x == x0 + 5:
                    try:
                        self.print_results()  # Show results thus far

                    # If user entered an invalid word, color problem letters red
                    except cheater.InvalidWordleLetters as exc:
                        invalid_letters = exc.invalid_letters

                        for _ in range(2):
                            for wl in invalid_letters:
                                self.print(x0 + wl.index, y, wl.letter.upper(), c="red")
                            self.move_cursor(x, y)
                            self.sleep(150)
                            for wl in invalid_letters:
                                self.print(
                                    x0 + wl.index, y, wl.letter.upper(), c=wl.color
                                )
                            self.move_cursor(x, y)
                            self.sleep(150)
                        continue

                    x = x0  # Reset horizontal position
                    y += 1  # Increment vertical position
                    self.print(x, y, "_____")  # Print blank line of underscores
                    self.move_cursor(x, y)  # Move cursor to beginning of line

            # Check if user pressed backspace
            elif self.is_backspace(c):
                # Don't do anything if we're at the beginning of the first line
                if x == x0 and y == y0:
                    continue

                # Check if we're at the beginning of a line
                if x == x0:
                    self.print(x, y, "     ")  # Clear line of underscores
                    x = x0 + 5  # Go to end of last line
                    y -= 1  # Go up one line
                    self.move_cursor(x, y)  # Move cursor to end of last line

                else:
                    x -= 1  # Move cursor back one
                    self.guesses.pop()  # Delete last guess
                    self.print(x, y, "_")  # Print underscore where letter used to be
                    self.move_cursor(x, y)  # Move cursor back over underscore

            # If we've typed five characters, only enter or backspace should do
            # anything, so ignore all other characters in this case.
            elif x == x0 + 5:
                continue

            # Check if user pressed space and wants a colored character
            elif c == " ":
                self.set_cursor_visibility(False)  # Hide cursor
                self.print(x, y, "_", c="yellow")  # Show a yellow underscore

                # If the user presses space again, they want a green colored character.
                # If they enter a letter, they want that letter to be yellow.  If they
                # do anything else, cancel the colored letter.
                c2 = self.get_key()

                # If second character pressed was a letter, enter that colored yellow
                if c2.upper() in english_letters:
                    self.print(x, y, c2.upper(), c="yellow")  # Print yellow character
                    self.set_cursor_visibility(True)  # Show cursor again

                    # Add guess to list
                    wl = cheater.WordleLetter(
                        letter=c2.lower(), color="yellow", index=x - x0
                    )
                    self.guesses.append(wl)
                    x += 1

                # Check if user pressed space and thus wants a green colored character
                elif c2 == " ":
                    self.print(x, y, "_", c="green")

                    # Need to get key a third time, and if anything other than a letter
                    # is pressed, cancel this entry.  If a letter is pressed, enter
                    # that letter colored green.
                    c3 = self.get_key()
                    if c3.upper() not in english_letters:
                        self.print(x, y, "_")  # Print uncolored underscore
                        self.move_cursor(x, y)  # Move cursor back over underscore
                        self.set_cursor_visibility(True)  # Show cursor again
                        continue

                    # If we get here, c3 is a letter, so enter it colored green
                    self.print(x, y, c3.upper(), c="green")
                    self.set_cursor_visibility(True)

                    # Add letter to list
                    wl = cheater.WordleLetter(
                        letter=c3.lower(), color="green", index=x - x0
                    )
                    self.guesses.append(wl)
                    x += 1  # Move cursor one over

                # If second character pressed was not a letter, uncolor and continue
                else:
                    self.print(x, y, "_")  # Uncolor underscore
                    self.move_cursor(x, y)  # Move cursor back over underscore
                    self.set_cursor_visibility(True)  # Show cursor again
                    continue

            # If we enter a letter without first pressing space, color it black
            elif c.upper() in english_letters:
                self.print(x, y, c.upper(), c="black")  # Show letter colored black
                wl = cheater.WordleLetter(letter=c.lower(), color="black", index=x - x0)
                self.guesses.append(wl)  # Add letter to list
                x += 1

        return self.guesses

    def get_results_string(self, max_rows=10, max_cols=8, sep="     "):
        """Get possible solutions formatted into columns.

        Parameters
        ----------
        max_rows : int, optional
            The maximum number of rows to display.  If the full string would require
            more than `max_rows` rows, show an ellipsis and the number of missing
            words on the last line instead.
        max_cols : int, optional
            The number of words per row.
        sep : str, optional
            The character(s) to put in between each column.  Defaults to '     '
            (five spaces) so the space in between each column is the same as the width
            of each column.

        Returns
        -------
        out_str : str
            The possible solutions formatted into a single string of rows and columns.
        """
        possible_words = cheater.cheat(self.guesses)
        out_str = format_words(
            possible_words, max_rows=max_rows, max_cols=max_cols, sep=sep
        )
        return out_str

    def print_title(self):  # pragma: no cover
        """Print title and instructions."""
        raise NotImplementedError

    def print_results(self):  # pragma: no cover
        """Print possible solutions given guesses."""
        raise NotImplementedError

    def print(self, x, y, string, c=None):  # pragma: no cover
        """Print a string at coordinates x, y.

        Parameters
        ----------
        x : int
            Horizontal position at which to print the string.
        y : int
            Height at which to print the string.
        string : str
            The string to print.
        c : str, {None, 'black', 'yellow', 'green', 'red'}
            The color in which to print.  Must be one of
            ['black', 'yellow', 'green', 'red'] or None. If `c` is None, it should
            print in the default color pair.
        """
        raise NotImplementedError

    def sleep(self, ms):  # pragma: no cover
        """Temporarily suspend execution.

        Parameters
        ----------
        ms : int
            Number of miliseconds before execution resumes.
        """
        raise NotImplementedError

    def move_cursor(self, x, y):  # pragma: no cover
        """Move cursor to position x, y.

        Parameters
        ----------
        x : int
            Desired horizontal position of cursor.
        y : int
            Desired vertical position of cursor.
        """
        raise NotImplementedError

    def set_cursor_visibility(self, visible):  # pragma: no cover
        """Set cursor visibility.

        Parameters
        ----------
        visible : bool
            Whether or not the cursor is visible.
        """
        raise NotImplementedError

    def get_key(self):  # pragma: no cover
        """Get a key press.

        Returns
        -------
        key : str
            The key that was pressed.

        # noqa : DAR202
        """
        raise NotImplementedError

    def is_enter(self, key):  # pragma: no cover
        """Check if `key` is the enter/return key.

        Parameters
        ----------
        key : str
            The key to check.

        Returns
        -------
        is_enter : bool
            True if `key` is the enter or return key, False otherwise.

        # noqa : DAR202
        """
        raise NotImplementedError

    def is_backspace(self, key):  # pragma: no cover
        """Check if `key` is the backspace/delete key.

        Parameters
        ----------
        key : str
            The key to check.

        Returns
        -------
        is_backspace : bool
            True if `key` is the backspace or delete key, False otherwise.

        # noqa : DAR202
        """
        raise NotImplementedError
