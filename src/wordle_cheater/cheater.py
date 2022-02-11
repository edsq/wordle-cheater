from dataclasses import dataclass
from typing import Optional
from wordle_cheater.dictionary import letters
from wordle_cheater.dictionary import wordle_words


@dataclass
class WordleLetter:
    letter: str
    color: str
    index: Optional[int] = None

    def __post_init__(self):
        # Parameter validation
        if self.letter.upper() not in letters:
            raise ValueError("`letter` must be an english letter.")

        if self.color not in ["black", "yellow", "green"]:
            raise ValueError("`color` must be one of ['black', 'yellow', 'green']")

        if not (isinstance(self.index, int) or self.index is None):
            raise ValueError("`index` must either be `None` or integer in range [0, 5)")

        if self.index not in range(5) and self.index is not None:
            raise ValueError("`index` must either be `None` or integer in range [0, 5)")

        # If color is black, index doesn't matter, so ensure it hasn't been set
        if self.color == "black" and self.index is not None:
            raise ValueError("`index` must be `None` if `color` is 'black'")


def check_word(
    word, blacks=None, yellows=None, greens=None, hard=True, check_dict=True
):
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

    assert len(yellows) == 5
    assert len(greens) == 5

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

        elif char in yellows[i]:
            return False

        elif greens[i] is not None and greens[i] != char:
            return False

    # Check if guess is a real word
    if check_dict:
        if word not in wordle_words:
            return False

    # If we've made it this far, the word is a possible solution
    return True


def find_words(blacks=None, yellows=None, greens=None):
    """Find all possible words that are consistent with current information.

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

    Returns
    -------
    possible_words : list
        List of possible solutions that match the given guesses.
    """
    possible_words = []
    for word in wordle_words:
        if check_word(word, blacks=blacks, yellows=yellows, greens=greens, hard=True):
            possible_words.append(word)

    return possible_words


def parse_wordle_letters(wordle_letters):
    """Parse and validate a list of WordleLetter objects.

    Positional arguments
    --------------------
    wordle_letters : list of WordleLetter objects
        The current guesses, a list of WordleLetter objects.

    Returns
    -------
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
    """

    blacks = []
    yellows = [[], [], [], [], []]
    greens = [None, None, None, None, None]

    # Get black characters first so we can check against them
    blacks = [wl.letter for wl in wordle_letters if wl.color == "black"]

    for wl in wordle_letters:
        if wl.color == "yellow":
            if wl.letter in blacks:
                raise ValueError(f"{wl.letter} appears as both black and yellow")

            yellows[wl.index].append(wl.letter)

        elif wl.color == "green":
            if wl.letter in blacks:
                raise ValueError(f"{wl.letter} appears as both black and green")

            if greens[wl.index] is not None and greens[wl.index] != wl.letter:
                raise ValueError(
                    f"{greens[index]} and {wl.letter} are both marked green in the same location"
                )

            greens[wl.index] = wl.letter

    return blacks, yellows, greens
