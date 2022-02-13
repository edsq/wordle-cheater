from wordle_cheater.interface_backend import WordleCheaterUI
from wordle_cheater.cheater import WordleLetter


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
        pass

    def print(self, x, y, string, c=None):
        if c is None:
            color_str = " " * len(string)

        elif c == "black":
            color_str = "b" * len(string)

        elif c == "yellow":
            color_str = "y" * len(string)

        elif c == "green":
            color_str = "g" * len(string)

        else:
            raise ValueError("`c` must be one of ['black', 'yellow', 'green'] or None.")

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


guesses = [
    ("b", "black", None),
    ("e", "yellow", 1),
    ("a", "black", None),
    ("t", "black", None),
    ("s", "black", None),
    ("o", "black", None),
    ("i", "black", None),
    ("l", "yellow", 2),
    ("e", "green", 3),
    ("d", "yellow", 4),
]
correct_wordle_letters = [WordleLetter(*guess) for guess in guesses]

correct_output = ["BEATS", "OILED", "     "]
correct_output_colors = ["bybbb", "bbygy", "     "]


def test_enter_letters():
    """Basic test of enter_letters()."""
    inputs = [
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

    test_ui = NoInterfaceUI(inputs=inputs)
    wordle_letters = test_ui.enter_letters()
    assert wordle_letters == correct_wordle_letters
    assert test_ui.output == correct_output
    assert test_ui.output_colors == correct_output_colors


def test_enter_letters_backspace():
    """Test handling of backspace and non-alpha characters in enter_letters()."""
    inputs = [
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

    test_ui = NoInterfaceUI(inputs=inputs)
    wordle_letters = test_ui.enter_letters()
    assert wordle_letters == correct_wordle_letters
    assert test_ui.output == correct_output
    assert test_ui.output_colors == correct_output_colors


def test_enter_letters_non_alpha():
    """Test handling of non-alpha characters in get_letters()."""
    inputs = [
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

    test_ui = NoInterfaceUI(inputs=inputs)
    wordle_letters = test_ui.enter_letters()
    assert wordle_letters == correct_wordle_letters
    assert test_ui.output == correct_output
    assert test_ui.output_colors == correct_output_colors


def test_get_results_string():
    """Basic test of get_results_string()."""
    test_ui = NoInterfaceUI(inputs=[])
    test_ui.guesses = correct_wordle_letters
    out_str = test_ui.get_results_string()
    assert out_str == "elder     dynel" or out_str == "dynel     elder"
