# Tests for cheater.parse_wordle_letters
import pytest
from wordle_cheater import __version__
from wordle_cheater.dictionary import wordle_words
from wordle_cheater.cheater import (
    WordleLetter,
    parse_wordle_letters,
    InvalidWordleLetters,
)

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]
counts = {"e": 1, "l": 1, "d": 1}


def test_parse_wordle_letters():
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
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens, parsed_counts = parse_wordle_letters(
        wordle_letters
    )
    assert parsed_blacks == blacks
    assert parsed_yellows == yellows
    assert parsed_greens == greens
    assert parsed_counts == counts


def test_parse_wordle_letters_repeated_yellow_black():
    """Test when a single word has the same character marked both yellow and black"""
    guesses = [
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
    ]
    these_counts = {"e": 1, "d": 1, "r": 1}
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens, parsed_counts = parse_wordle_letters(
        wordle_letters
    )
    assert parsed_blacks == [["b"], [], ["a"], ["t", "a"], ["s", "d"]]
    assert parsed_yellows == [["d"], ["e", "r"], ["e"], [], []]
    assert parsed_greens == [None, None, None, None, None]
    assert parsed_counts == these_counts


def test_parse_wordle_letters_repeated_yellow_green():
    """Test when a single word has the same character marked both yellow and green"""
    guesses = [
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
    ]
    these_counts = {"e": 2}
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens, parsed_counts = parse_wordle_letters(
        wordle_letters
    )
    assert parsed_blacks == [["b", "w"], ["o"], ["a", "w"], ["t"], ["s"]]
    assert parsed_yellows == [[], ["e"], [], [], ["e"]]
    assert parsed_greens == [None, None, None, "e", None]
    assert parsed_counts == these_counts


def test_parse_wordle_letters_repeated_green_black():
    """Test when a single word has the same character marked both green and black."""
    guesses = [
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
    ]
    these_counts = {"e": 1, "r": 1}
    wordle_letters = [WordleLetter(*guess) for guess in guesses]
    parsed_blacks, parsed_yellows, parsed_greens, parsed_counts = parse_wordle_letters(
        wordle_letters
    )
    assert parsed_blacks == [["b", "r"], ["i"], ["a", "v"], ["t"], ["s"]]
    assert parsed_yellows == [[], ["e"], [], [], []]
    assert parsed_greens == [None, None, None, "e", "r"]
    assert parsed_counts == these_counts


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)


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
    with pytest.raises(InvalidWordleLetters):
        _ = parse_wordle_letters(wordle_letters)
