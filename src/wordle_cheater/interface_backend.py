import wordle_cheater.cheater as cheater
from wordle_cheater.dictionary import letters as english_letters


class WordleCheaterUI:
    """Base class for handling logic of interface, independent of output method."""

    def __init__(self):
        self.guesses = []  # List of WordleLetter objects representing current guesses.
        self.curs_x = 0  # x position of cursor
        self.curs_y = 0  # y position of cursor
        self.entering_letters = False  # Whether or not we're entering previous guesses

    def main(self, *args, **kwargs):
        """Main entry point; called by the CLI."""
        self.print_title()
        self.enter_letters()
        self.print_results()

    def enter_letters(self, x0=0, y0=0):
        """Base method for entering previous guesses with a wordle-like interface.

        This method both returns and sets `self.guesses`.

        Keyword arguments
        -----------------
        x0 : int
            The horizontal position of the upper-left corner of the words to enter.
        y0 : int
            The vertical position of the upper-left corner of the words to enter.

        Returns
        -------
        guesses : list of WordleLetter objects
        """
        self.curs_x, self.curs_y = (
            x0,
            y0,
        )  # Location of cursor.  (0, 0) is top left corner.
        self.print(
            self.curs_x, self.curs_y, "_____"
        )  # Start with a blank line of underscores
        self.move_cursor(self.curs_x, self.curs_y)
        self.guesses = []
        self.entering_letters = True
        while self.entering_letters:
            # Get keypress
            c = self.get_key()

            # Check if user pressed return
            if self.is_enter(c):
                # Check if we've entered all 6 words
                if self.curs_y == y0 + 5 and self.curs_x == x0 + 5:
                    self.entering_letters = False  # Exit loop

                # Check if user pressed return on an empty line and wants to exit
                elif self.curs_x == x0:
                    self.set_cursor_visibility(False)  # Hide cursor
                    self.print(
                        self.curs_x, self.curs_y, "     "
                    )  # Clear line of underscores
                    self.entering_letters = False  # Exit loop

                # Check if user pressed return on a full line and wants another
                elif self.curs_x == x0 + 5:
                    self.print_results()  # Show results thus far
                    self.curs_x = x0  # Reset horizontal position
                    self.curs_y += 1  # Increment vertical position
                    self.print(
                        self.curs_x, self.curs_y, "_____"
                    )  # Print blank line of underscores
                    self.move_cursor(
                        self.curs_x, self.curs_y
                    )  # Move cursor to beginning of line

            # Check if user pressed backspace
            elif self.is_backspace(c):
                # Don't do anything if we're at the beginning of the first line
                if self.curs_x == x0 and self.curs_y == y0:
                    continue

                # Check if we're at the beginning of a line
                if self.curs_x == x0:
                    self.print(
                        self.curs_x, self.curs_y, "     "
                    )  # Clear line of underscores
                    self.curs_x = x0 + 5  # Go to end of last line
                    self.curs_y -= 1  # Go up one line
                    self.move_cursor(
                        self.curs_x, self.curs_y
                    )  # Move cursor to end of last line

                else:
                    self.curs_x -= 1  # Move cursor back one
                    self.guesses.pop()  # Delete last guess
                    self.print(
                        self.curs_x, self.curs_y, "_"
                    )  # Print underscore where letter used to be
                    self.move_cursor(
                        self.curs_x, self.curs_y
                    )  # Move cursor back over underscore

            # If we've typed five characters, only enter or backspace should do
            # anything, so ignore all other characters in this case.
            elif self.curs_x == x0 + 5:
                continue

            # Check if user pressed space and wants a colored character
            elif c == " ":
                self.set_cursor_visibility(False)  # Hide cursor
                self.print(
                    self.curs_x, self.curs_y, "_", c="yellow"
                )  # Show a yellow underscore

                # If the user presses space again, they want a green colored character.
                # If they enter a letter, they want that letter to be yellow.  If they
                # do anything else, cancel the colored letter.
                c2 = self.get_key()

                # If second character pressed was a letter, enter that colored yellow
                if c2.upper() in english_letters:
                    self.print(
                        self.curs_x, self.curs_y, c2.upper(), c="yellow"
                    )  # Print yellow character
                    self.set_cursor_visibility(True)  # Show cursor again

                    # Add guess to list
                    wl = cheater.WordleLetter(
                        letter=c2.lower(), color="yellow", index=self.curs_x - x0
                    )
                    self.guesses.append(wl)
                    self.curs_x += 1

                # Check if user pressed space and thus wants a green colored character
                elif c2 == " ":
                    self.print(self.curs_x, self.curs_y, "_", c="green")

                    # Need to get key a third time, and if anything other than a letter
                    # is pressed, cancel this entry.  If a letter is pressed, enter
                    # that letter colored green.
                    c3 = self.get_key()
                    if c3.upper() not in english_letters:
                        self.print(
                            self.curs_x, self.curs_y, "_"
                        )  # Print uncolored underscore
                        self.move_cursor(
                            self.curs_x, self.curs_y
                        )  # Move cursor back over underscore
                        self.set_cursor_visibility(True)  # Show cursor again
                        continue

                    # If we get here, c3 is a letter, so enter it colored green
                    self.print(self.curs_x, self.curs_y, c3.upper(), c="green")
                    self.set_cursor_visibility(True)

                    # Add letter to list
                    wl = cheater.WordleLetter(
                        letter=c3.lower(), color="green", index=self.curs_x - x0
                    )
                    self.guesses.append(wl)
                    self.curs_x += 1  # Move cursor one over

                # If second character pressed was not a letter, uncolor and continue
                else:
                    self.print(self.curs_x, self.curs_y, "_")  # Uncolor underscore
                    self.set_cursor_visibility(True)  # Show cursor again
                    continue

            # If we enter a letter without first pressing space, color it black
            elif c.upper() in english_letters:
                self.print(
                    self.curs_x, self.curs_y, c.upper(), c="black"
                )  # Show letter colored black
                wl = cheater.WordleLetter(letter=c.lower(), color="black", index=None)
                self.guesses.append(wl)  # Add letter to list
                self.curs_x += 1

        return self.guesses

    def get_results_string(self, max_rows=10, cols=8, sep="     "):
        """Get possible solutions formatted into columns.

        Keyword arguments
        -----------------
        max_rows : int
            The maximum number of rows to display.  If the full string would require
            more than `max_rows` rows, show an ellipsis and the number of missing
            words on the last line instead.
        cols : int
            The number of words per row.
        sep : str
            The character(s) to put in between each column.  Defaults to '     '
            (five spaces) so the space in between each column is the same as the width
            of each column.

        Returns
        -------
        out_str : str
            The possible solutions formatted into a single string of rows and columns.
        """
        blacks, yellows, greens = cheater.parse_wordle_letters(self.guesses)
        possible_words = cheater.find_words(blacks, yellows, greens)

        lines = [
            sep.join(possible_words[i : i + cols])
            for i in range(0, len(possible_words), cols)
        ]
        if len(lines) > max_rows:
            lines = lines[: max_rows - 1]
            n_missing = int(len(possible_words) - (cols * len(lines)))
            out_str = "\n".join(lines)
            out_str += f"\n...({n_missing} more)"
        else:
            out_str = "\n".join(lines)

        return out_str

    def print_title(self):
        """Print title and instructions."""
        raise NotImplementedError

    def print_results(self):
        """Print possible solutions given guesses."""
        raise NotImplementedError

    def print(self, x, y, string, c=None):
        """Print a string at coordinates x, y.

        Positional arguments
        --------------------
        x : int
            Horizontal position at which to print the string.
        y : int
            Height at which to print the string.
        string : str
            The string to print.

        Keyword arguments
        -----------------
        c : str
            The color in which to print.  Must be one of ['black', 'yellow', 'green']
            or None. If `c` is None, it should print in the default color pair.
        """
        raise NotImplementedError

    def move_cursor(self, x, y):
        """Move cursor to position x, y.

        Positional arguments
        --------------------
        x : int
            Desired horizontal position of cursor.
        y : int
            Desired vertical position of cursor.
        """
        raise NotImplementedError

    def set_cursor_visibility(self, visible):
        """Set cursor visibility.

        Positional arguments
        --------------------
        visible : boolean
            Whether or not the cursor is visible.
        """
        raise NotImplementedError

    def get_key(self):
        """Get a key press.

        Returns
        -------
        key : str
            The key that was pressed.
        """
        raise NotImplementedError

    def is_enter(self, key):
        """Check if `key` is the enter/return key.

        Positional arguments
        --------------------
        key : str
            The key to check.

        Returns
        -------
        is_enter : boolean
            True if `key` is the enter or return key, False otherwise.
        """
        raise NotImplementedError

    def is_backspace(self, key):
        """Check if `key` is the backspace/delete key.

        Positional arguments
        --------------------
        key : str
            The key to check.

        Returns
        -------
        is_backspace : boolean
            True if `key` is the backspace or delete key, False otherwise.
        """
        raise NotImplementedError