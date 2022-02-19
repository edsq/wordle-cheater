# Miscellaneous tests for cheater.py
from wordle_cheater import __version__
from wordle_cheater.dictionary import wordle_words
from wordle_cheater.cheater import find_words

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = ["b", "a", "t", "s", "o", "i"]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]


def test_version():
    assert __version__ == "0.1.0"


def test_wordle_dictionary():
    assert len(wordle_words) == 12972


def test_find_words():
    words = find_words(blacks=blacks, yellows=yellows, greens=greens)
    assert sorted(words) == ["dynel", "elder"]
