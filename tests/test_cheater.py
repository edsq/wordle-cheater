"""Miscellaneous tests for cheater.py."""
import pytest
from wordle_cheater.cheater import (
    easy_cheat,
    find_words,
    get_wordle_letters,
    WordleGuesses,
    WordleLetter,
)
from wordle_cheater.dictionary import wordle_dictionary

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]
counts = dict()

wordle_guesses = WordleGuesses()
wordle_guesses.blacks = blacks
wordle_guesses.yellows = yellows
wordle_guesses.greens = greens
wordle_guesses.counts = counts


def test_wordle_dictionary():
    """Length of the Wordle dictionary is correct."""
    assert len(wordle_dictionary) == 12972


def test_find_words():
    """It returns 'dynel' and 'elder'."""
    words = find_words(wordle_guesses)
    assert sorted(words) == ["dynel", "elder"]


def test_wordle_letter_comparison():
    """Test that we can create WordleLetter objects and compare two."""
    wl_1 = WordleLetter("a", "black", 0)
    wl_2 = WordleLetter("a", "black", 1)
    assert wl_2 > wl_1


def test_invalid_wordle_letter_non_alpha():
    """Test that WordleLetter raises an error when given a non-alpha character."""
    with pytest.raises(ValueError) as exc_info:
        _ = WordleLetter("$", "black", 0)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`letter` must be an english letter."


def test_invalid_wordle_letter_uppercase():
    """Test that WordleLetter raises an error when given an uppercase character."""
    with pytest.raises(ValueError) as exc_info:
        _ = WordleLetter("A", "black", 0)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`letter` must be lowercase."


def test_invalid_wordle_letter_color():
    """Test that WordleLetter raises an error when given an invalid color."""
    with pytest.raises(ValueError) as exc_info:
        _ = WordleLetter("a", "white", 0)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0] == "`color` must be one of ['black', 'yellow', 'green']"
    )


def test_invalid_wordle_letter_non_int():
    """Test that WordleLetter raises an error when given a non-integer."""
    with pytest.raises(ValueError) as exc_info:
        _ = WordleLetter("a", "black", 1.5)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`index` must be integer in range [0, 5)"


def test_invalid_wordle_letter_index_out_of_range():
    """Test that WordleLetter raises an error when given an index too high."""
    with pytest.raises(ValueError) as exc_info:
        _ = WordleLetter("a", "black", 6)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`index` must be integer in range [0, 5)"


def test_get_wordle_letters():
    """Test the get_wordle_letters convenience function."""
    wls = get_wordle_letters("abc", "byg")
    correct_wls = [
        WordleLetter("a", "black", 0),
        WordleLetter("b", "yellow", 1),
        WordleLetter("c", "green", 2),
    ]
    assert wls == correct_wls


def test_get_wordle_letters_invalid():
    """Test when an invalid color character is given."""
    with pytest.raises(ValueError) as exc_info:
        _ = get_wordle_letters("a", "w")
    assert (
        exc_info.value.args[0] == "`colors` must contain only 'b', 'y', or 'g' (got w)."
    )


def test_easy_cheat():
    """Test the easy_cheat convenience function."""
    solutions = easy_cheat("beats oiled", "bybbb bbygy")
    assert sorted(solutions) == sorted(["elder", "dynel"])
