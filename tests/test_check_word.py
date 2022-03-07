# Tests for cheater.check_word
import pytest
from wordle_cheater.cheater import check_word


# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]

invalid_words = [
    "craft",  # Invalid as letters marked black
    "ruled",  # Invalid as yellow letters reused
    "elude",  # Invalid as green letter doesn't appear
    "cruel",  # Invalid as yellow letters don't appear (hard mode)
    "eeeee",  # Invalid due to word not in word list
]


def test_check_word_valid():
    # Testing with solution from 02-07-2022
    assert check_word(
        "elder",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=True,
        check_dict=True,
    )


@pytest.mark.parametrize("word", invalid_words)
def test_check_word_invalid(word):
    """Test words that should be invalid given blacks, yellows, greens."""
    assert not check_word(
        word,
        blacks=blacks,
        yellows=yellows,
        greens=greens,
    )


def test_check_word_two_repeated_letters():
    # Test if check_word properly handles when two letters repeat
    # Guess: "array", answer: "aroma"
    blacks = [
        [],
        [],
        ["r"],
        [],
        ["y"],
    ]  # second r marked black as it only appears in answer once
    yellows = [
        [],
        [],
        [],
        ["a"],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = ["a", "r", None, None, None]
    counts = {"a": 2, "r": 1}
    assert check_word(
        "aroma", blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


def test_check_word_green_and_black():
    # Test if check_word properly handles when a letter is marked both green and black
    # Guess: "berry", answer: "score"
    blacks = [["b"], [], ["r"], [], ["y"]]
    yellows = [
        [],
        ["e"],
        [],
        [],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, "r", None]
    counts = {"r": 1}
    assert check_word(
        "score", blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


def test_check_word_green_and_yellow():
    # Test if check_word properly handles when a letter is marked both green and yellow
    # Guess: "berry", answer: "roars"
    blacks = [["b"], ["e"], [], [], ["y"]]
    yellows = [
        [],
        [],
        ["r"],
        [],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, "r", None]
    counts = {"r": 2}
    assert check_word("roars", blacks=blacks, yellows=yellows, greens=greens)


def test_check_word_yellow_and_black():
    # Test if check_word properly handles when a letter is marked both green and yellow
    # Guess: "array", answer: "leash"
    blacks = [["a"], ["r"], ["r"], [], ["y"]]
    yellows = [
        [],
        [],
        [],
        ["a"],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, None, None]
    counts = {"a": 1}
    assert check_word(
        "leash", blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


def test_check_word_green_yellow_black():
    # Test if check_word properly handles when a letter is marked all three colors
    # Guess: "sassy", answer: "shops"
    blacks = [[], ["a"], [], ["s"], ["y"]]
    yellows = [
        [],
        [],
        ["s"],
        [],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = ["s", None, None, None, None]
    counts = {"s": 2}
    assert check_word(
        "shops", blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


def test_check_word_invalid_too_many_repeated():
    # Test if repeating a letter too many times is marked as invalid
    # Guess: "array", answer: "right"
    # The word "river" should be found invalid, since only one of the two "r"s was
    # colored, thus we know the answer has only one r
    blacks = [["a"], [], ["r"], ["a"], ["y"]]
    yellows = [
        [],
        ["r"],
        [],
        [],
        [],
    ]
    greens = [None, None, None, None, None]
    counts = {"r": 1}
    assert not check_word(
        "river",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        check_dict=False,
        counts=counts,
    )


def test_check_word_invalid_not_enough_repeated():
    # Test if repeating a letter not enough times is marked as invalid
    # Guess: "array", answer: "corer"
    # The word "strip" should be found invalid, since we know the answer
    # should have two "r"s
    blacks = [["a"], [], [], ["a"], ["y"]]
    yellows = [
        [],
        ["r"],
        [],
        [],
        [],
    ]
    greens = [None, None, "r", None, None]
    counts = {"r": 2}
    assert not check_word(
        "strip", blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


def test_check_word_invalid_repeated_black_conflict():
    # Test that when repeated letters appear in the previous guesses, words with
    # a character marked black at the same location will still be invalid
    # Guess: "array", answer: "right"
    # The word "lores" should be marked invalid, as the second "r" in array was
    # Marked black
    blacks = [["a"], [], ["r"], ["a"], ["y"]]
    yellows = [
        [],
        ["r"],
        [],
        [],
        [],
    ]
    greens = [None, None, None, None, None]
    assert not check_word("lores", blacks=blacks, yellows=yellows, greens=greens)
