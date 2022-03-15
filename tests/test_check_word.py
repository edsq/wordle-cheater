"""Tests for cheater.check_word()."""
import pytest

from wordle_cheater.cheater import WordleGuesses, check_word


def get_wordle_guesses(blacks, yellows, greens, counts):
    """Get the appropriate WordleGuesses object."""
    wordle_guesses = WordleGuesses()
    wordle_guesses.blacks = blacks
    wordle_guesses.yellows = yellows
    wordle_guesses.greens = greens
    wordle_guesses.counts = counts
    return wordle_guesses


# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = [["b", "o"], ["i"], ["a"], ["t"], ["s"]]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]


# Words that should be invalid given above blacks, yellows, greens
invalid_words = {
    "black_conflict": "craft",  # Invalid as letters marked black
    "yellow_conflict": "ruled",  # Invalid as yellow letters reused
    "no_green": "elude",  # Invalid as green letter doesn't appear
    "hard_mode": "cruel",  # Invalid as yellow letters don't appear (hard mode)
    "word_list": "ldzez",  # Invalid due to word not in word list
}


# Parameters for testing valid words when letters in guesses repeat
# Values are `(blacks, yellows, greens, counts, word)`
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
    """A valid word given `blacks`, `yellows`, `greens`, `counts` is 'elder'."""
    # Testing with solution from 02-07-2022
    wordle_guesses = get_wordle_guesses(blacks, yellows, greens, counts=dict())
    assert check_word("elder", wordle_guesses, check_dict=True)


@pytest.mark.parametrize("word", invalid_words.values(), ids=invalid_words.keys())
def test_check_word_invalid(word):
    """Test words that should be invalid given blacks, yellows, greens."""
    wordle_guesses = get_wordle_guesses(blacks, yellows, greens, counts=dict())
    assert not check_word(word, wordle_guesses)


@pytest.mark.parametrize(
    "blacks,yellows,greens,counts,word",
    valid_repeated_params.values(),
    ids=valid_repeated_params.keys(),
)
def test_check_word_valid_repeating(blacks, yellows, greens, counts, word):
    """Test valid words when guesses have repeated letters."""
    wordle_guesses = get_wordle_guesses(blacks, yellows, greens, counts)
    assert check_word(word, wordle_guesses)


@pytest.mark.parametrize(
    "blacks,yellows,greens,counts,word",
    invalid_repeated_params.values(),
    ids=invalid_repeated_params.keys(),
)
def test_check_word_invalid_repeating(blacks, yellows, greens, counts, word):
    """Test invalid words due to repeated letters in guesses."""
    wordle_guesses = get_wordle_guesses(blacks, yellows, greens, counts)
    assert not check_word(word, wordle_guesses)


def test_check_word_no_guesses():
    """Test that check_word works even if we don't supply any guesses."""
    wordle_guesses = WordleGuesses()
    assert check_word("beats", wordle_guesses)


def test_check_word_no_dict():
    """Test that check_word works when we don't require a real word."""
    wordle_guesses = get_wordle_guesses(blacks, yellows, greens, counts=dict())
    assert check_word("ldzez", wordle_guesses, check_dict=False)
