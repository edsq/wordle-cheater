from wordle_cheater import __version__

def test_version():
    assert __version__ == '0.1.0'

def test_get_words():
    from wordle_cheater.wordle_cheater import get_words
    words = get_words()
    assert len(words) == 3213
