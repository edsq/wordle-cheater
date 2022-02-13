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
        super().__init__()

    def print_title(self):
        pass

    def print_results(self):
        pass

    def print(self, x, y, string, c=None):
        pass

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


def test_enter_letters():
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

    inputs = [
        "b",
        " ",
        "e",
        "a",
        "t",
        "s",
        "\r",
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

    test_ui = NoInterfaceUI(inputs=inputs)
    wordle_letters = test_ui.enter_letters()
    assert wordle_letters == correct_wordle_letters
