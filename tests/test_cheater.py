# Miscellaneous tests for cheater.py
import pytest
from wordle_cheater import __version__
from wordle_cheater.dictionary import wordle_words
from wordle_cheater.cheater import find_words, WordleLetter

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]


def test_version():
    assert __version__ == "0.1.0"


def test_wordle_dictionary():
    assert len(wordle_words) == 12972


def test_find_words():
    words = find_words(blacks=blacks, yellows=yellows, greens=greens)
    assert sorted(words) == ["dynel", "elder"]


def test_wordle_letter_comparison():
    """Test that we can create WordleLetter objects and compare two."""
    wl_1 = WordleLetter("a", "black", 0)
    wl_2 = WordleLetter("a", "black", 1)
    assert wl_2 > wl_1


def test_invalid_wordle_letter_non_alpha():
    """Test that WordleLetter raises an error when given a non-alpha character."""
    with pytest.raises(ValueError) as exc_info:
        wl = WordleLetter("$", "black", 0)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`letter` must be an english letter."


def test_invalid_wordle_letter_uppercase():
    """Test that WordleLetter raises an error when given an uppercase character."""
    with pytest.raises(ValueError) as exc_info:
        wl = WordleLetter("A", "black", 0)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`letter` must be lowercase."


def test_invalid_wordle_letter_color():
    """Test that WordleLetter raises an error when given an invalid color."""
    with pytest.raises(ValueError) as exc_info:
        wl = WordleLetter("a", "white", 0)
    assert exc_info.type is ValueError
    assert (
        exc_info.value.args[0] == "`color` must be one of ['black', 'yellow', 'green']"
    )


def test_invalid_wordle_letter_non_int():
    """Test that WordleLetter raises an error when given a non-integer."""
    with pytest.raises(ValueError) as exc_info:
        wl = WordleLetter("a", "black", 1.5)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`index` must be integer in range [0, 5)"


def test_invalid_wordle_letter_index_out_of_range():
    """Test that WordleLetter raises an error when given an index too high."""
    with pytest.raises(ValueError) as exc_info:
        wl = WordleLetter("a", "black", 6)
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "`index` must be integer in range [0, 5)"
