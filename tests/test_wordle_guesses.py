"""Tests for cheater.WordleGuesses."""
import pytest

from wordle_cheater.cheater import InvalidWordleLetters, WordleGuesses, WordleLetter

# Parameters for testing valid entries into WordleGuesses
# Values are (guesses, blacks, yellows, greens, counts)
valid_params = {
    "basic_parse": (
        # Wordle from 02-07-2022 (solution 'elder')
        # My guesses were 'beats', 'oiled', 'elder'
        [
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
        ],
        [["b", "o"], ["i"], ["a"], ["t"], ["s"]],
        [[], ["e"], ["l"], [], ["d"]],
        [None, None, None, "e", None],
        {"e": 1, "l": 1, "d": 1},
    ),
    "repeated_black_yellow": (
        [
            ("b", "black", 0),
            ("e", "yellow", 1),
            ("a", "black", 2),
            ("t", "black", 3),
            ("s", "black", 4),
            ("d", "yellow", 0),  # d marked yellow as it appears in "elder"
            ("r", "yellow", 1),
            ("e", "yellow", 2),
            ("a", "black", 3),
            ("d", "black", 4),  # d marked black as it only appears once in "elder"
        ],
        [["b"], [], ["a"], ["t", "a"], ["s", "d"]],
        [["d"], ["e", "r"], ["e"], [], []],
        [None, None, None, None, None],
        {"e": 1, "d": 1, "r": 1},
    ),
    "repeated_yellow_green": (
        [
            ("b", "black", 0),
            ("e", "yellow", 1),
            ("a", "black", 2),
            ("t", "black", 3),
            ("s", "black", 4),
            ("w", "black", 0),
            ("o", "black", 1),
            ("w", "black", 2),
            ("e", "green", 3),  # e marked green as it appears here in "elder"
            ("e", "yellow", 4),  # e also appears at beginning of "elder"
        ],
        [["b", "w"], ["o"], ["a", "w"], ["t"], ["s"]],
        [[], ["e"], [], [], ["e"]],
        [None, None, None, "e", None],
        {"e": 2},
    ),
    "repeated_black_green": (
        [
            ("b", "black", 0),
            ("e", "yellow", 1),
            ("a", "black", 2),
            ("t", "black", 3),
            ("s", "black", 4),
            ("r", "black", 0),  # r marked black as it appears only once in "elder"
            ("i", "black", 1),
            ("v", "black", 2),
            ("e", "green", 3),
            ("r", "green", 4),  # r marked green as it appears here in "elder"
        ],
        [["b", "r"], ["i"], ["a", "v"], ["t"], ["s"]],
        [[], ["e"], [], [], []],
        [None, None, None, "e", "r"],
        {"e": 1, "r": 1},
    ),
}


# Parameters for testing invalid sets of WordleLetters
# Values are (guesses, invalid_indices)
invalid_params = {
    "black_green": (  # Black letter marked green
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "black", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("r", "black", 0),
            ("i", "black", 1),
            ("v", "black", 2),
            ("e", "green", 3),  # e was marked black in first word, but here is green
            ("r", "black", 4),
        ],
        [3],
    ),
    "black_yellow": (  # Black letter marked yellow
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "black", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("r", "black", 0),
            ("i", "black", 1),
            ("v", "black", 2),
            ("e", "yellow", 3),  # e was marked black in first word, but here is yellow
            ("r", "black", 4),
        ],
        [3],
    ),
    "green_black": (  # Green letter marked black
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "green", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("r", "black", 0),
            ("i", "black", 1),
            ("v", "black", 2),
            ("e", "black", 3),  # e was marked green in first word, but here is black
            ("r", "black", 4),
        ],
        [3],
    ),
    "yellow_black": (  # Yellow letter marked black
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "yellow", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("r", "black", 0),
            ("i", "black", 1),
            ("v", "black", 2),
            ("e", "black", 3),  # e was marked yellow in first word, but here is black
            ("r", "black", 4),
        ],
        [3],
    ),
    "yellow_green": (  # Yellow letter marked green
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "yellow", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("s", "black", 0),
            ("t", "black", 1),
            ("e", "green", 2),  # e was marked yellow in first word, but now is green
            ("a", "black", 3),
            ("l", "black", 4),
        ],
        [2],
    ),
    "green_yellow": (  # Green letter marked yellow
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "green", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("s", "black", 0),
            ("t", "black", 1),
            ("e", "yellow", 2),  # e was marked green in first word, but now is yellow
            ("a", "black", 3),
            ("l", "black", 4),
        ],
        [2],
    ),
    "multiple": (  # Two conflicting guesses
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "green", 2),
            ("a", "black", 3),
            ("m", "black", 4),
            ("s", "black", 0),
            ("t", "black", 1),
            ("e", "yellow", 2),  # e was marked green in first word, but now is yellow
            ("a", "green", 3),  # a was marked black in first word, but now is green
            ("l", "black", 4),
        ],
        [2, 3],
    ),
    "green_conflict": (  # Two different letters marked green in same location
        [
            ("d", "black", 0),
            ("r", "black", 1),
            ("e", "black", 2),
            ("a", "green", 3),  # a marked as green
            ("m", "black", 4),
            ("d", "black", 0),
            ("o", "black", 1),
            ("u", "black", 2),
            ("s", "green", 3),  # s marked green - conflicts with a
            ("e", "black", 4),
        ],
        [3],
    ),
}


@pytest.mark.parametrize(
    "guesses,blacks,yellows,greens,counts",
    valid_params.values(),
    ids=valid_params.keys(),
)
def test_wordle_guesses_valid(guesses, blacks, yellows, greens, counts):
    """`WordleGuesses` has correct `blacks`, `yellows`, `greens`, `counts`."""
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    wordle_guesses = WordleGuesses(wordle_letters)
    assert wordle_guesses.blacks == blacks
    assert wordle_guesses.yellows == yellows
    assert wordle_guesses.greens == greens
    assert wordle_guesses.counts == counts


@pytest.mark.parametrize(
    "guesses,invalid_indices", invalid_params.values(), ids=invalid_params.keys()
)
def test_wordle_guesses_invalid(guesses, invalid_indices):
    """It raises an `InvalidWordleLetters` exception."""
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    invalid_letters = [wordle_letters[5 + i] for i in invalid_indices]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = WordleGuesses(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted(invalid_letters)


def test_wordle_guesses_invalid_length():
    """Test that we raise a ValueError when given an invalid number of letters."""
    wordle_letters = [WordleLetter("a", "black", 0)]
    with pytest.raises(ValueError) as exc_info:
        _ = WordleGuesses(wordle_letters)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0]
        == "`len(wordle_letters)` must be an integer multiple of five"
    )


def test_add_word_invalid_length():
    """It raises a ValueError when given an invalid number of letters."""
    wordle_letters = [WordleLetter("a", "black", 0)]
    wordle_guesses = WordleGuesses()
    with pytest.raises(ValueError) as exc_info:
        wordle_guesses.add_word(wordle_letters)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0]
        == "`word` must be a length-5 list of WordleLetter objects."
    )


def test_get_invalid_letters_invalid_length():
    """It raises a ValueError when given an invalid number of letters."""
    guesses = valid_params["basic_parse"][0]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    wordle_guesses = WordleGuesses(wordle_letters)

    word_to_check = [WordleLetter("a", "black", 0)]  # should be length 5
    with pytest.raises(ValueError) as exc_info:
        _ = wordle_guesses.get_invalid_letters(word_to_check)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0]
        == "`word` must be a length-5 list of WordleLetter objects."
    )
