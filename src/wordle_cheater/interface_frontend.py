import curses
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


if __name__ == "__main__":
    curses_ui = CursesInterface()
    curses.wrapper(curses_ui.main)
