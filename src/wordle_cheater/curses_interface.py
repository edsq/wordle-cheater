import curses
from wordle_cheater.dictionary import letters
import wordle_cheater.cheater as cheater


def print_after_cursor(stdscr, y, x, string, *args, **kwargs):
    """Print `string` at x, y and move cursor back to x, y."""
    stdscr.addstr(y, x, string, *args, **kwargs)
    stdscr.move(y, x)


def center_print(stdscr, y, string, *args, **kwargs):
    """Print `string` at y in center of `stdscr`."""
    height, width = stdscr.getmaxyx()

    str_length = len(string)
    x_mid = width // 2

    stdscr.addstr(y, x_mid - str_length // 2, string, *args, **kwargs)


def main(stdscr):
    center_print(stdscr, 1, "Wordle Cheater :(", curses.A_BOLD)
    center_print(stdscr, 2, "Enter guesses below.")
    center_print(stdscr, 3, "spacebar: change color", curses.A_DIM)

    height, width = stdscr.getmaxyx()
    guesses = enter_letters(stdscr, y0=5, x0=width // 2 - 3)

    from wordle_cheater.interface import get_results

    get_results(guesses)


def enter_letters(stdscr, y0=0, x0=0):
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # White on yellow
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)  # White on green

    for i in range(6):
        print_after_cursor(stdscr, y0 + i, x0, "_____")
    stdscr.move(y0, x0)
    stdscr.refresh()

    guesses = []
    char_index = 0
    entering_guesses = True
    while entering_guesses:
        c = stdscr.getkey()

        if c == curses.KEY_ENTER or c == "\n" or c == "\r":
            # Return pressed
            if len(guesses) == 30 and char_index == 5:
                # We've used all 6 guesses
                entering_guesses = False

            elif char_index == 0:
                # We've hit return on an empty line and want to exit
                entering_guesses = False

            elif char_index == 5:
                # We've entered a full word and want a new line (pressed return)
                char_index = 0
                print_after_cursor(stdscr, y0 + len(guesses) // 5, x0, "_____")

        elif (c == curses.KEY_BACKSPACE or c == "\b" or c == "\x7f") and char_index > 0:
            # Backspace pressed - ignore this if we're at the beginning of the line already
            char_index -= 1
            guesses.pop()
            print_after_cursor(stdscr, y0 + len(guesses) // 5, x0 + char_index, "_")

        elif char_index == 5:
            # Only return and delete do anything if we've typed 5 characters already
            continue

        elif c == " ":
            # Space pressed - we want to enter a colored character
            curses.curs_set(False)
            print_after_cursor(
                stdscr,
                y0 + len(guesses) // 5,
                x0 + char_index,
                "_",
                curses.color_pair(2),
            )  # show yellow underscore

            c = stdscr.getkey()
            if c == " ":
                # Space pressed again - we want to enter a green character
                print_after_cursor(
                    stdscr,
                    y0 + len(guesses) // 5,
                    x0 + char_index,
                    "_",
                    curses.color_pair(3),
                )  # show green underscore

                c = stdscr.getkey()
                if c.upper() not in letters:
                    # Non-letter character pressed - uncolor underscore and continue
                    print_after_cursor(
                        stdscr, y0 + len(guesses) // 5, x0 + char_index, "_"
                    )
                    curses.curs_set(True)
                    continue

                # Print character with green background
                stdscr.addstr(
                    y0 + len(guesses) // 5,
                    x0 + char_index,
                    c.upper(),
                    curses.color_pair(3),
                )
                curses.curs_set(True)

                # Add guess to list
                wl = cheater.WordleLetter(
                    letter=c.lower(), color="green", index=char_index
                )
                guesses.append(wl)
                char_index += 1

            elif c.upper() in letters:
                # Letter pressed - we want to enter a yellow character
                # Print character with yellow background
                stdscr.addstr(
                    y0 + len(guesses) // 5,
                    x0 + char_index,
                    c.upper(),
                    curses.color_pair(2),
                )
                curses.curs_set(True)

                # Add guess to list
                wl = cheater.WordleLetter(
                    letter=c.lower(), color="yellow", index=char_index
                )
                guesses.append(wl)
                char_index += 1

            else:
                # Non-letter character pressed - uncolor underscore and continue
                print_after_cursor(stdscr, y0 + len(guesses) // 5, x0 + char_index, "_")
                curses.curs_set(True)
                continue

        elif c.upper() in letters:
            # We want to enter a "black" colored character
            stdscr.addstr(
                y0 + len(guesses) // 5, x0 + char_index, c.upper(), curses.color_pair(1)
            )

            wl = cheater.WordleLetter(letter=c.lower(), color="black", index=None)
            guesses.append(wl)
            char_index += 1

        stdscr.refresh()

    return guesses


if __name__ == "__main__":
    curses.wrapper(main)
