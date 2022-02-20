# Tests for cheater.parse_wordle_letters
import pytest
from wordle_cheater import __version__
from wordle_cheater.dictionary import wordle_words
from wordle_cheater.cheater import (
    WordleLetter,
    parse_wordle_letters,
    InvalidWordleLetter,
)

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = ["b", "a", "t", "s", "o", "i"]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]


def test_parse_wordle_letters():
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
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(wordle_letters)
    assert parsed_blacks == blacks
    assert parsed_yellows == yellows
    assert parsed_greens == greens


def test_parse_wordle_letters_repeated_yellow_black():
    """Test when a single word has the same character marked both yellow and black"""
    guesses = [
        ("b", "black", None),
        ("e", "yellow", 1),
        ("a", "black", None),
        ("t", "black", None),
        ("s", "black", None),
        ("d", "yellow", 0),  # d marked yellow as it appears in "elder"
        ("r", "yellow", 1),
        ("e", "yellow", 2),
        ("a", "black", None),
        ("d", "black", None),  # d marked black as it only appears once in "elder"
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(wordle_letters)
    assert parsed_blacks == ["b", "a", "t", "s", "a", "d"]
    assert parsed_yellows == [["d"], ["e", "r"], ["e"], [], []]
    assert parsed_greens == [None, None, None, None, None]


def test_parse_wordle_letters_repeated_yellow_green():
    """Test when a single word has the same character marked both yellow and green"""
    guesses = [
        ("b", "black", None),
        ("e", "yellow", 1),
        ("a", "black", None),
        ("t", "black", None),
        ("s", "black", None),
        ("w", "black", None),
        ("o", "black", None),
        ("w", "black", None),
        ("e", "green", 3),  # e marked green as it appears here in "elder"
        ("e", "yellow", 4),  # e also appears at beginning of "elder"
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(wordle_letters)
    assert parsed_blacks == ["b", "a", "t", "s", "w", "o", "w"]
    assert parsed_yellows == [[], ["e"], [], [], ["e"]]
    assert parsed_greens == [None, None, None, "e", None]


def test_parse_wordle_letters_repeated_green_black():
    """Test when a single word has the same character marked both green and black."""
    guesses = [
        ("b", "black", None),
        ("e", "yellow", 1),
        ("a", "black", None),
        ("t", "black", None),
        ("s", "black", None),
        ("r", "black", None),  # r marked black as it appears only once in "elder"
        ("i", "black", None),
        ("v", "black", None),
        ("e", "green", 3),
        ("r", "green", 4),  # r marked green as it appears here in "elder"
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(wordle_letters)
    assert parsed_blacks == ["b", "a", "t", "s", "r", "i", "v"]
    assert parsed_yellows == [[], ["e"], [], [], []]
    assert parsed_greens == [None, None, None, "e", "r"]


def test_parse_wordle_letters_invalid_black_green():
    """Test when a character is marked black and then green in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "black", None),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "green", 3),  # e was marked black in first word, but here is green
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )


def test_parse_wordle_letters_invalid_black_yellow():
    """Test when a character is marked black and then yellow in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "black", None),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "yellow", 3),  # e was marked black in first word, but here is yellow
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )


def test_parse_wordle_letters_invalid_green_black():
    """Test when a character is marked green and then black in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "green", 3),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "black", None),  # e was marked green in first word, but here is black
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )


def test_parse_wordle_letters_invalid_yellow_black():
    """Test when a character is marked yellow and then black in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "yellow", 3),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "black", None),  # e was marked yellow in first word, but here is black
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )


def test_parse_wordle_letters_invalid_yellow_green():
    """Test when a character is marked yellow and then green in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "yellow", 3),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "green", 3),  # e was marked yellow here in first word, but now is green
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )


def test_parse_wordle_letters_invalid_yellow_green():
    """Test when a character is marked green and then yellow in two different words."""
    guesses = [
        ("d", "black", None),
        ("r", "black", None),
        ("e", "green", 3),
        ("a", "black", None),
        ("m", "black", None),
        ("r", "black", None),
        ("i", "black", None),
        ("v", "black", None),
        ("e", "yellow", 3),  # e was marked yellow here in first word, but now is green
        ("r", "black", None),
    ]
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    with pytest.raises(InvalidWordleLetter):
        parsed_blacks, parsed_yellows, parsed_greens = parse_wordle_letters(
            wordle_letters
        )
