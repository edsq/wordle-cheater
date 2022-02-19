# Tests for cheater.check_word
from wordle_cheater.cheater import check_word


# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = ["b", "a", "t", "s", "o", "i"]
yellows = [[], ["e"], ["l"], [], ["d"]]
greens = [None, None, None, "e", None]


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


def test_check_word_invalid_black():
    # An invalid guess due to letters being marked black
    assert not check_word(
        "craft",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=False,
        check_dict=False,
    )


def test_check_word_invalid_yellow():
    # An invalid guess due to yellow letters being reused
    assert not check_word(
        "ruled",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=False,
        check_dict=False,
    )


def test_check_word_invalid_green():
    # An invalid guess due to a letter marked green not appearing
    assert not check_word(
        "elude",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=False,
        check_dict=False,
    )


def test_check_word_invalid_hardmode():
    # An invalid guess due to not reusing yellow letters
    assert not check_word(
        "cruel",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=True,
        check_dict=False,
    )


def test_check_word_invalid_wordlist():
    # An invalid guess due to the word not being in the dictionary
    assert not check_word(
        "eeeee",
        blacks=blacks,
        yellows=yellows,
        greens=greens,
        hard=False,
        check_dict=True,
    )


def test_check_word_two_repeated_letters():
    # Test if check_word properly handles when two letters repeat
    # Guess: "array", answer: "aroma"
    blacks = ["r", "y"]  # second r marked black as it only appears in answer once
    yellows = [
        [],
        [],
        [],
        ["a"],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = ["a", "r", None, None, None]
    assert check_word("aroma", blacks=blacks, yellows=yellows, greens=greens)


def test_check_word_green_and_black():
    # Test if check_word properly handles when a letter is marked both green and black
    # Guess: "berry", answer: "score"
    blacks = ["b", "r", "y"]
    yellows = [
        [],
        ["e"],
        [],
        [],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, "r", None]
    assert check_word("score", blacks=blacks, yellows=yellows, greens=greens)


def test_check_word_green_and_yellow():
    # Test if check_word properly handles when a letter is marked both green and yellow
    # Guess: "berry", answer: "roars"
    blacks = ["b", "e", "y"]
    yellows = [
        [],
        [],
        ["r"],
        [],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, "r", None]
    assert check_word("roars", blacks=blacks, yellows=yellows, greens=greens)


def test_check_word_yellow_and_black():
    # Test if check_word properly handles when a letter is marked both green and yellow
    # Guess: "array", answer: "leash"
    blacks = ["a", "r", "r", "y"]
    yellows = [
        [],
        [],
        [],
        ["a"],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = [None, None, None, None, None]
    assert check_word("leash", blacks=blacks, yellows=yellows, greens=greens)


def test_check_word_green_yellow_black():
    # Test if check_word properly handles when a letter is marked all three colors
    # Guess: "sassy", answer: "shops"
    blacks = ["a", "s", "y"]
    yellows = [
        [],
        [],
        [],
        ["s"],
        [],
    ]  # second a marked yellow as it appears in answer in a different position
    greens = ["s", None, None, None, None]
    assert check_word("shops", blacks=blacks, yellows=yellows, greens=greens)