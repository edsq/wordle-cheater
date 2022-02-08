from wordle_cheater import __version__
from wordle_cheater.dictionary import wordle_words
from wordle_cheater.wordle_cheater import check_word
from wordle_cheater.wordle_cheater import find_words

# Wordle from 02-07-2022 (solution 'elder')
# My guesses were 'beats', 'oiled', 'elder'
blacks = ['b', 'a', 't', 's', 'o', 'i']
yellows = [[], ['e'], ['l'], [], ['d']]
greens = [None, None, None, 'e', None]

def test_version():
    assert __version__ == '0.1.0'

def test_wordle_dictionary():
    assert len(wordle_words) == 12972

def test_check_word_valid():
    # Testing with solution from 02-07-2022
    assert check_word('elder',
                      blacks=blacks,
                      yellows=yellows,
                      greens=greens,
                      hard=True,
                      check_dict=True,
                     )

def test_check_word_invalid_black():
    # An invalid guess due to letters being marked black
    assert not check_word('craft',
                          blacks=blacks,
                          yellows=yellows,
                          greens=greens,
                          hard=False,
                          check_dict=False,
                         )

def test_check_word_invalid_yellow():
    # An invalid guess due to yellow letters being reused
    assert not check_word('ruled',
                          blacks=blacks,
                          yellows=yellows,
                          greens=greens,
                          hard=False,
                          check_dict=False,
                         )

def test_check_word_invalid_green():
    # An invalid guess due to a letter marked green not appearing
    assert not check_word('elude',
                          blacks=blacks,
                          yellows=yellows,
                          greens=greens,
                          hard=False,
                          check_dict=False,
                         )

def test_check_word_invalid_hardmode():
    # An invalid guess due to not reusing yellow letters
    assert not check_word('cruel',
                          blacks=blacks,
                          yellows=yellows,
                          greens=greens,
                          hard=True,
                          check_dict=False,
                         )

def test_check_word_invalid_wordlist():
    # An invalid guess due to the word not being in the dictionary
    assert not check_word('eeeee',
                          blacks=blacks,
                          yellows=yellows,
                          greens=greens,
                          hard=False,
                          check_dict=True,
                         )

def test_find_words():
    words = find_words(blacks=blacks, yellows=yellows, greens=greens)
    assert sorted(words) == ['dynel', 'elder']
