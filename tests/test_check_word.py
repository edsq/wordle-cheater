# Tests for cheater.check_word
import pytest
from wordle_cheater.cheater import check_word


# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]

# Words that should be invalid given above blacks, yellows, greens
invalid_words = [
    "craft",  # Invalid as letters marked black
    "ruled",  # Invalid as yellow letters reused
    "elude",  # Invalid as green letter doesn't appear
    "cruel",  # Invalid as yellow letters don't appear (hard mode)
    "eeeee",  # Invalid due to word not in word list
]

# Parameters for testing valid words when letters in guesses repeat
# Values are `(blacks, yellows, greens, counts, answer)`
valid_repeated_params = {
    "two_repeated_letters": (  # Guess: 'array', answer: 'aroma'
        [[], [], ["r"], [], ["y"]],
        [[], [], [], ["a"], []],
        ["a", "r", None, None, None],
        {"a": 2, "r": 1},
        "aroma",
    ),
    "black_and_green": (  # Guess: "berry", answer: "score"
        [["b"], [], ["r"], [], ["y"]],
        [[], ["e"], [], [], []],
        [None, None, None, "r", None],
        {"r": 1},
        "score",
    ),
    "yellow_and_green": (  # Guess: "berry", answer: "roars"
        [["b"], ["e"], [], [], ["y"]],
        [[], [], ["r"], [], []],
        [None, None, None, "r", None],
        {"r": 2},
        "roars",
    ),
    "black_and_yellow": (  # Guess: "array", answer: "leash"
        [["a"], ["r"], ["r"], [], ["y"]],
        [[], [], [], ["a"], []],
        [None, None, None, None, None],
        {"a": 1},
        "leash",
    ),
    "black_yellow_green": (  # Guess: "sassy", answer: "shops"
        [[], ["a"], [], ["s"], ["y"]],
        [[], [], ["s"], [], []],
        ["s", None, None, None, None],
        {"s": 2},
        "shops",
    ),
}

# Parameters for testing invalid words due to repeated letters in guesses
# Values are `(blacks, yellows, greens, counts, word)`
invalid_repeated_params = {
    "too_many_repeated": (  # Guess: "array", answer: "right"
        # Test if repeating a letter too many times is marked as invalid
        # The word "river" should be found invalid, since only one of the two "r"s was
        # colored, thus we know the answer has only one r
        [["a"], [], ["r"], ["a"], ["y"]],
        [[], ["r"], [], [], []],
        [None, None, None, None, None],
        {"r": 1},
        "river",
    ),
    "not_enough_repeated": (  # Guess: "array", answer: "corer"
        # Test if repeating a letter not enough times is marked as invalid
        # The word "strip" should be found invalid, since we know the answer
        # should have two "r"s
        [["a"], [], [], ["a"], ["y"]],
        [[], ["r"], [], [], []],
        [None, None, "r", None, None],
        {"r": 2},
        "strip",
    ),
    "repeated_black_conflict": (  # Guess: "array", answer: "right"
        # Test that when repeated letters appear in the previous guesses, words with
        # a character marked black at the same location will still be invalid
        # The word "lores" should be marked invalid, as the second "r" in array was
        # marked black
        [["a"], [], ["r"], ["a"], ["y"]],
        [[], ["r"], [], [], []],
        [None, None, None, None, None],
        {"r": 1},
        "lores",
    ),
}


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


@pytest.mark.parametrize(
    "blacks,yellows,greens,counts,answer",
    valid_repeated_params.values(),
    ids=valid_repeated_params.keys(),
)
def test_check_word_valid_repeating(blacks, yellows, greens, counts, answer):
    """Test valid words when guesses have repeated letters."""
    assert check_word(
        answer, blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )


@pytest.mark.parametrize(
    "blacks,yellows,greens,counts,word",
    invalid_repeated_params.values(),
    ids=invalid_repeated_params.keys(),
)
def test_check_word_valid_repeating(blacks, yellows, greens, counts, word):
    """Test invalid words due to repeated letters in guesses."""
    assert not check_word(
        word, blacks=blacks, yellows=yellows, greens=greens, counts=counts
    )
