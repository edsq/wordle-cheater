from english_words import english_words_lower_alpha_set as all_words

def get_words():
    return {word for word in all_words if len(word) == 5}

def check_word(word, blacks=None, yellows=None, greens=None, hard=True, check_dict=True):
    """Check if `word` is a possible solution given previous guesses.
    
    All inputs must be lowercase as we don't bother to cast them to lowercase to save a bit of time.

    Positional arguments
    -------------------
    word : length-5 string
        The word to check.

    Keyword arguments
    ----------------
    blacks : list
        A list of lowercase letters that are not in the word.
    yellows : length-5 list of lists
        Lowercase letters that are in the word, but not in the correct location.  For example, if
        our guesses tell us that the letter 'A' was in the word, but it was not the third letter, we
        would pass `yellows = [[], [], ['a'], [], []]`.
    greens : length-5 list
        Lowercase letters that are in the word and in the correct location.  For example, if our
        guesses tell us that the letter 'A' is the fourth letter of the word, we would pass
        `greens = [None, None, None, 'a', None]`.
    hard : boolean
        Whether or not to use wordle 'hard mode' rules, requiring that all letters in `yellows` and
        `greens` must be in `word`.
    check_dict : boolean
        Whether or not to check if `word` is a real five letter english word.

    Returns
    -------
    valid : boolean
        Whether or not `word` is a possible solution given `blacks`, `yellows`, and `greens`.
    """

    if blacks is None:
        blacks = []
    
    if yellows is None:
        yellows = [[], [], [], [], []]

    if greens is None:
        greens = [None, None, None, None, None]

    # Check for hard mode compliance
    if hard:
        known_chars = [char for position in yellows for char in position]
        known_chars += [char for char in greens if char is not None]
        for known_char in known_chars:
            if known_char not in word:
                return False

    # Now check each letter for compatibility with known information
    for i, char in enumerate(word):
        if char in blacks:
            return False

        elif yellows[i] == char:
            return False

        elif greens[i] is not None and greens[i] != char:
            return False

    # Check if guess is a real word
    if check_dict:
        all_words = get_words()
        if word not in all_words:
            return False

    # If we've made it this far, the word is a possible solution
    return True
