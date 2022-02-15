import curses
import click
from wordle_cheater.interface_backend import WordleCheaterUI


class CursesInterface(WordleCheaterUI):
    def main(self, stdscr):
        self.stdscr = stdscr
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White on black
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Black on yellow
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Black on green

        height, width = stdscr.getmaxyx()
        self.results_window = curses.newwin(
            height - 12, width, 12, 0
        )  # window for printing results

        x0 = width // 2 - 3
        y0 = 5
        self.print_title()
        self.enter_letters(x0=x0, y0=y0)
        self.print_results()
        self.set_cursor_visibility(False)
        self.get_key()

    def center_print(self, y, string, *args, **kwargs):
        height, width = self.stdscr.getmaxyx()

        str_length = len(string)
        x_mid = width // 2

        self.stdscr.addstr(y, x_mid - str_length // 2, string, *args, **kwargs)

    def print_title(self):
        self.center_print(1, "Wordle Cheater :(", curses.A_BOLD)
        self.center_print(2, "Enter guesses below.")
        self.center_print(3, "spacebar: change color", curses.A_DIM)

    def print_results(self, sep="     "):
        height, width = self.results_window.getmaxyx()
        max_rows = height - 1  # -1 to account for "Possible solutions" header
        cols = width // (5 + len(sep))

        out_str = self.get_results_string(max_rows=max_rows, cols=cols, sep=sep)

        self.results_window.clear()
        self.results_window.addstr(0, 0, "Possible solutions:", curses.A_UNDERLINE)
        self.results_window.addstr(1, 0, out_str)
        self.results_window.refresh()

    def print(self, x, y, string, c=None):
        if c is None:
            self.stdscr.addstr(y, x, string)

        elif c == "black":
            self.stdscr.addstr(y, x, string, curses.color_pair(1))

        elif c == "yellow":
            self.stdscr.addstr(y, x, string, curses.color_pair(2))

        elif c == "green":
            self.stdscr.addstr(y, x, string, curses.color_pair(3))

        else:
            raise ValueError("`c` must be one of ['black', 'yellow', 'green'] or None.")

    def move_cursor(self, x, y):
        self.stdscr.move(y, x)

    def set_cursor_visibility(self, visible):
        curses.curs_set(visible)

    def get_key(self):
        return self.stdscr.getkey()

    def is_enter(self, key):
        if key == curses.KEY_ENTER or key == "\n" or key == "\r":
            return True

        else:
            return False

    def is_backspace(self, key):
        if key == curses.KEY_BACKSPACE or key == "\b" or key == "\x7f":
            return True

        else:
            return False


class ClickInterface(WordleCheaterUI):
    """Interface for using Click alone to enter letters and see solutions."""

    def __init__(self, max_rows=10, cols=8, x0=4, y0=4, esc="\033"):
        self.max_rows = max_rows
        self.cols = 8
        self.x0 = x0  # Initial x position of guesses
        self.y0 = y0  # Initial y position of guesses
        self.esc = esc  # ANSI escape code
        self._curs_xy = (0, 0)  # cursor position
        self.line_lengths = [0]  # Highest x values we've hit per line
        super().__init__()

    @property
    def curs_xy(self):
        """Location of cursor."""
        return self._curs_xy

    @curs_xy.setter
    def curs_xy(self, xy):
        """Update max line lengths when we update cursor position."""
        x, y = xy
        if y > len(self.line_lengths) - 1:
            self.line_lengths += [0 for i in range(y - len(self.line_lengths) + 1)]

        if x > self.line_lengths[y]:
            self.line_lengths[y] = x

        self._curs_xy = xy

    def main(self):
        self.print_title()
        self.enter_letters(x0=self.x0, y0=self.y0)
        self.print_results()
        self.set_cursor_visibility(True)

    def print_title(self):
        self.print(0, 0, "Wordle Cheater :(", bold=True)
        self.print(0, 1, "Enter guesses below.")
        self.print(0, 2, "spacebar: change color", dim=True)

    def print_results(self):
        # If we're still entering letters, don't do anything
        if self.entering_letters:
            return

        out_str = self.get_results_string(
            max_rows=self.max_rows, cols=self.cols, sep="     "
        )

        self.move_cursor(0, self.curs_xy[1] + 1)
        click.secho("Possible solutions:", underline=True)
        click.echo(out_str)

    def print(self, x, y, string, c=None, *args, **kwargs):
        # Move cursor to x, y so we can print there
        self.move_cursor(x, y)

        if c is None:
            click.secho(string, nl=False, *args, **kwargs)

        elif c == "black":
            click.secho(string, fg="white", bg="black", nl=False)

        elif c == "yellow":
            click.secho(string, fg="black", bg="yellow", nl=False)

        elif c == "green":
            click.secho(string, fg="black", bg="green", nl=False)

        self.curs_xy = (self.curs_xy[0] + len(string), self.curs_xy[1])

    def move_cursor(self, x, y):
        # Check if we want to move cursor up (decreasing y)
        if self.curs_xy[1] > y:
            click.echo(f"{self.esc}[{self.curs_xy[1] - y}A", nl=False)

        # Check if we want to move cursor down (increasing y)
        elif self.curs_xy[1] < y:
            # Check if we need to add new lines to screen
            if len(self.line_lengths) - 1 < y:
                click.echo("\n" * (y - self.curs_xy[1]), nl=False)

                # New line, so definitely need to print spaces to move x
                click.echo(" " * x, nl=False)
                self.curs_xy = (x, y)
                return

            else:
                # Should just arrow down to not overwrite stuff
                click.echo(f"{self.esc}[{y - self.curs_xy[1]}B", nl=False)

        # Check if we want to move cursor left (decreasing x)
        if self.curs_xy[0] > x:
            click.echo(f"{self.esc}[{self.curs_xy[0] - x}D", nl=False)

        # Check if we want to move cursor right (increasing x)
        elif self.curs_xy[0] < x:
            # Check if we need to add space to right of cursor
            if self.line_lengths[y] > x:
                click.echo(" " * x, nl=False)

            else:
                # Should just arrow to right to not overwrite stuff
                click.echo(f"{self.esc}[{x - self.curs_xy[0]}C", nl=False)

        self.curs_xy = (x, y)

    def set_cursor_visibility(self, visible):
        if visible:
            click.echo(f"{self.esc}[?25h", nl=False)

        else:
            click.echo(f"{self.esc}[?25l", nl=False)

    def get_key(self):
        return click.getchar()

    def is_enter(self, key):
        if key == "\r" or key == "\n":
            return True

        else:
            return False

    def is_backspace(self, key):
        if key == "\b" or key == "\x7f":
            return True

        else:
            return False


if __name__ == "__main__":
    # curses_ui = CursesInterface()
    # curses.wrapper(curses_ui.main)
    click_ui = ClickUI()
    click_ui.main()
