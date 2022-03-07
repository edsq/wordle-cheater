# Tests for cheater.parse_wordle_letters
import pytest
from wordle_cheater.cheater import (
    WordleLetter,
    parse_wordle_letters,
    InvalidWordleLetters,
)

# Parameters for testing valid entries into parse_wordle_letters
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


@pytest.mark.parametrize(
    "guesses,blacks,yellows,greens,counts",
    valid_params.values(),
    ids=valid_params.keys(),
)
def test_parse_wordle_letters_valid(guesses, blacks, yellows, greens, counts):
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens, parsed_counts = parse_wordle_letters(
        wordle_letters
    )
    assert parsed_blacks == blacks
    assert parsed_yellows == yellows
    assert parsed_greens == greens
    assert parsed_counts == counts


def test_parse_wordle_letters_invalid_black_green():
    """Test when a character is marked black and then green in two different words."""
    guesses = [
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
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-2]])


def test_parse_wordle_letters_invalid_black_yellow():
    """Test when a character is marked black and then yellow in two different words."""
    guesses = [
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
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-2]])


def test_parse_wordle_letters_invalid_green_black():
    """Test when a character is marked green and then black in two different words."""
    guesses = [
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
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-2]])


def test_parse_wordle_letters_invalid_yellow_black():
    """Test when a character is marked yellow and then black in two different words."""
    guesses = [
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
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-2]])


def test_parse_wordle_letters_invalid_yellow_green():
    """Test when a character is marked yellow and then green in two different words."""
    guesses = [
        ("d", "black", 0),
        ("r", "black", 1),
        ("e", "yellow", 2),
        ("a", "black", 3),
        ("m", "black", 4),
        ("s", "black", 0),
        ("t", "black", 1),
        ("e", "green", 2),  # e was marked yellow here in first word, but now is green
        ("a", "black", 3),
        ("l", "black", 4),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-3]])


def test_parse_wordle_letters_invalid_green_yellow():
    """Test when a character is marked green and then yellow in two different words."""
    guesses = [
        ("d", "black", 0),
        ("r", "black", 1),
        ("e", "green", 2),
        ("a", "black", 3),
        ("m", "black", 4),
        ("s", "black", 0),
        ("t", "black", 1),
        ("e", "yellow", 2),  # e was marked green here in first word, but now is yellow
        ("a", "black", 3),
        ("l", "black", 4),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-3]])


def test_parse_wordle_letters_invalid_multiple():
    """Test when more than one character is invalid."""
    guesses = [
        ("d", "black", 0),
        ("r", "black", 1),
        ("e", "green", 2),
        ("a", "black", 3),
        ("m", "black", 4),
        ("s", "black", 0),
        ("t", "black", 1),
        ("e", "yellow", 2),  # e was marked green here in first word, but now is yellow
        ("a", "green", 3),  # a was marked black here in first word, but now is green
        ("l", "black", 4),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted(
        [wordle_letters[-3], wordle_letters[-2]]
    )


def test_parse_wordle_letters_invalid_green_conflict():
    """Test when two different letters are marked green in the same location."""
    guesses = [
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
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetters) as exc_info:
        _ = parse_wordle_letters(wordle_letters)
    assert sorted(exc_info.value.invalid_letters) == sorted([wordle_letters[-2]])
