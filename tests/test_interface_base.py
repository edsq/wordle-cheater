import pytest
from wordle_cheater.interface_base import WordleCheaterUI, format_words
from wordle_cheater.cheater import WordleLetter, parse_wordle_letters


class NoInterfaceUI(WordleCheaterUI):
    """Class for testing WordleCheaterUI."""

    def __init__(self, inputs):
        """Constructor for TestUI class.

        Positional Arguments
        --------------------
        inputs : list
            A list of characters, to be read off sequentially as inputs by get_key().
        """
        self.inputs = inputs[::-1]  # Reverse order so we can just pop to get inputs
        self.output = [""]  # List of strings of output, each element a new line.
        self.output_colors = [""]  # List of colors of output
        super().__init__()

    def print_title(self):
        pass

    def print_results(self):
        # Have to try parsing guesses to look for invalid entries
        blacks, yellows, greens, counts = parse_wordle_letters(self.guesses)

    def print(self, x, y, string, c=None):
        if c is None:
            color_str = " " * len(string)

        elif c == "black":
            color_str = "b" * len(string)

        elif c == "yellow":
            color_str = "y" * len(string)

        elif c == "green":
            color_str = "g" * len(string)

        elif c == "red":
            color_str = "r" * len(string)

        else:
            raise ValueError(
                "`c` must be one of ['black', 'yellow', 'green', 'red'] or None."
            )

        # Add new lines if needed
        if y >= len(self.output):
            new_lines_needed = 1 + y - len(self.output)
            self.output += ["" for i in range(new_lines_needed)]
            self.output_colors += ["" for i in range(new_lines_needed)]

        # Now "Print"
        self.output[y] = self.output[y][:x] + string + self.output[y][x + len(string) :]
        self.output_colors[y] = (
            self.output_colors[y][:x]
            + color_str
            + self.output_colors[y][x + len(color_str) :]
        )

    def move_cursor(self, x, y):
        pass

    def set_cursor_visibility(self, visible):
        pass

    def get_key(self):
        return self.inputs.pop()

    def is_enter(self, key):
        if key == "\r":
            return True

        else:
            return False

    def is_backspace(self, key):
        if key == "\b":
            return True

        else:
            return False

    def sleep(self, ms):
        pass


guesses = [
    ("b", "black", 0),
    ("e", "yellow", 1),
    ("a", "black", 2),
    ("t", "black", 3),
    ("s", "black", 4),
    ("o", "black", 0),
    ("i", "black", 1),
    ("l", "yellow", 2),
    ("e", "green", 3),
    ("d", "yellow", 4),
]
correct_wordle_letters = [WordleLetter(*guess) for guess in guesses]

correct_output = ["BEATS", "OILED", "     "]
correct_output_colors = ["bybbb", "bbygy", "     "]


test_inputs = {
    "basic": (
        [
            "B",
            " ",
            "e",
            "a",
            "T",
            "s",
            "X",  # Should do nothing as we've already entered five characters
            "\r",
            "o",
            "i",
            "\r",  # Should do nothing as we aren't at the end of a word
            " ",
            "l",
            " ",
            " ",
            "e",
            " ",
            "D",
            "\r",
            "\r",
        ]
    ),
    "backspace": (  # Test handling of backspace
        [
            "\b",  # Shouldn't do anything, as we're at the beginning of first line
            "X",  # wrong character
            "\b",  # delete X
            "b",  # right character
            " ",
            "X",  # wrong character, colored yellow
            "\b",  # delete yellow X
            " ",
            "e",  # enter yellow E
            "a",
            "t",
            "X",  # wrong character
            "\r",  # enter pressed
            "\b",  # go back to previous line
            "\b",  # delete X
            "s",  # correct character
            "\r",
            "o",
            "X",  # wrong character
            "X",  # second wrong character
            "\b",
            "\b",  # delete both wrong characters
            "i",
            " ",
            "l",
            " ",
            " ",
            "X",  # wrong character, colored green
            "\b",  # delete green X
            " ",
            " ",
            "e",  # correct character
            " ",
            "d",
            "\r",
            "\r",
        ]
    ),
    "non_alpha": (  # Test handling of non-alpha characters
        [
            "&",  # Should be ignored
            " ",
            "&",  # Should cancel the yellow colored character
            "B",
            " ",
            "e",
            " ",
            " ",
            "&",  # Should cancel the green colored character
            "a",
            "T",
            "s",
            "&",  # Should do nothing
            "\r",
            "o",
            "i",
            " ",
            "l",
            " ",
            " ",
            "e",
            " ",
            "D",
            "\r",
            "\r",
        ]
    ),
    "invalid": (  # Try entering an invalid word, then delete it
        [
            "b",
            " ",
            "e",  # E colored yellow,
            "a",
            "t",
            "s",
            "\r",
            "b",
            " ",
            " ",
            "e",  # E colored green - invalid!
            "a",
            "t",
            "s",
            "\r",  # This should effectively do nothing, since E is invalid
            "\b",
            "\b",
            "\b",
            "\b",
            "\b",  # Delete this word
            "o",
            "i",
            " ",
            "l",
            " ",
            " ",
            "e",
            " ",
            "d",
            "\r",
            "\r",
        ]
    ),
}


@pytest.mark.parametrize("inputs", test_inputs.values(), ids=test_inputs.keys())
def test_enter_letters(inputs):
    """Test that inputs are correctly parsed."""
    test_ui = NoInterfaceUI(inputs=inputs)
    test_ui.main()
    wordle_letters = test_ui.guesses
    assert wordle_letters == correct_wordle_letters
    assert test_ui.output == correct_output
    assert test_ui.output_colors == correct_output_colors


def test_enter_letters_six_words():
    """Test that we exit after entering six words."""
    correct_wordle_letters = 6 * [WordleLetter("a", "black", i) for i in range(5)]
    correct_output = 6 * ["AAAAA"]
    correct_output_colors = 6 * ["bbbbb"]

    inputs = 6 * ["a", "a", "a", "a", "a", "\r"]
    test_ui = NoInterfaceUI(inputs=inputs)
    test_ui.main()
    wordle_letters = test_ui.guesses
    assert wordle_letters == correct_wordle_letters
    assert test_ui.output == correct_output
    assert test_ui.output_colors == correct_output_colors


def test_get_results_string():
    """Basic test of get_results_string()."""
    test_ui = NoInterfaceUI(inputs=[])
    test_ui.guesses = correct_wordle_letters
    out_str = test_ui.get_results_string()
    assert out_str == "elder     dynel" or out_str == "dynel     elder"


def test_format_words():
    """Basic test of format_words."""
    out_str = format_words(
        ["a", "b", "c", "d", "e", "f", "g"], max_rows=3, max_cols=3, sep=" "
    )
    assert out_str == "a b c\nd e f\ng"


def test_format_words_truncate():
    """Test when format_words must truncate some words."""
    out_str = format_words(
        ["a", "b", "c", "d", "e", "f", "g"], max_rows=2, max_cols=3, sep=" "
    )
    assert out_str == "a b c\n...(4 more)"
