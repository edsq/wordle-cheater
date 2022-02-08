from wordle_cheater import __version__

def test_version():
    assert __version__ == '0.1.0'

def test_wordle_dictionary():
    from wordle_cheater.dictionary import wordle_words
    assert len(wordle_words) == 12972
