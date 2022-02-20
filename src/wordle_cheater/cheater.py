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

        if not self.letter.lower() == self.letter:
            raise ValueError("`letter` must be lowercase.")

        if self.color not in ["black", "yellow", "green"]:
            raise ValueError("`color` must be one of ['black', 'yellow', 'green']")

        if not (isinstance(self.index, int)):
            raise ValueError("`index` must be integer in range [0, 5)")

        if self.index not in range(5):
            raise ValueError("`index` must be integer in range [0, 5)")


class InvalidWordleLetter(Exception):
    def __init__(self, message, wordle_letter):
        self.invalid_letter = wordle_letter
        super().__init__(message)


def _flatten(l):
    """Flatten a list of lists into a 1D list."""
    return [item for sublist in l for item in sublist]


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

    # Get unraveled yellows
    all_yellows = [c for position in yellows for c in position]

    # Check for hard mode compliance
    if hard:
        known_chars = all_yellows + [char for char in greens if char is not None]
        for known_char in known_chars:
            if known_char not in word:
                return False

    # Now check each letter for compatibility with known information
    for i, char in enumerate(word):
        # Can only have black letters if those letters also appear as a yellow or green
        if char in blacks and char not in all_yellows and char != greens[i]:
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
        The current guesses, a list of WordleLetter objects.  Must be from an integer
        number of words, so `len(wordle_letters)` must be an integer multiple of 5.

    Returns
    -------
    blacks : length-5 list of lists
        A list of lowercase letters that are not in the word.  For example, if our
        guesses have the letter 'A' marked black at the second character,
        `yellows = [[], ['A'], [], [], []]`.
    yellows : length-5 list of lists
        Lowercase letters that are in the word, but not in the correct location.  For
        example, if our guesses tell us that the letter 'A' was in the word, but it was
        not the third letter, `yellows = [[], [], ['a'], [], []]`.
    greens : length-5 list
        Lowercase letters that are in the word and in the correct location.  For
        example, if our guesses tell us that the letter 'A' is the fourth letter of the
        word, `greens = [None, None, None, 'a', None]`.
    """

    blacks = [[], [], [], [], []]
    yellows = [[], [], [], [], []]
    greens = [None, None, None, None, None]

    if len(wordle_letters) % 5 != 0:
        raise ValueError("`len(wordle_letters)` must be an integer multiple of five")

    words = [wordle_letters[i * 5 : i * 5 + 5] for i in range(len(wordle_letters) // 5)]

    for word in words:
        these_blacks = [wl for wl in word if wl.color == "black"]
        these_yellows = [wl for wl in word if wl.color == "yellow"]
        these_greens = [wl for wl in word if wl.color == "green"]

        # Validate black letters
        for wl in these_blacks:
            if wl.letter in yellows[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked black and yellow in the same location",
                    wl,
                )

            if wl.letter == greens[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked black and green in the same location",
                    wl,
                )

            # A black character could have been previously colored only if it is also
            # colored at least as many times in this word as in previous words
            if wl.letter in _flatten(yellows) or wl.letter in greens:
                num_prev_colored = len([l for l in _flatten(yellows) if l == wl.letter])
                num_prev_colored += len([l for l in greens if l == wl.letter])
                num_curr_colored = len(
                    [_wl for _wl in these_yellows if _wl.letter == wl.letter]
                )
                num_curr_colored += len(
                    [_wl for _wl in these_greens if _wl.letter == wl.letter]
                )

                if num_prev_colored > num_curr_colored:
                    raise InvalidWordleLetter(
                        f"'{wl.letter.upper()}' marked black but previously colored", wl
                    )

        # Validate yellow letters
        for wl in these_yellows:
            if wl.letter in blacks[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked yellow and black in the same location",
                    wl,
                )

            if wl.letter == greens[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked yellow and green in the same location",
                    wl,
                )

            # A yellow character could have been previously marked black only if it was also previously colored
            if wl.letter in _flatten(blacks) and (
                wl.letter not in _flatten(yellows) or wl.letter not in greens
            ):
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked yellow but previously marked black",
                    wl,
                )

        # Validate green letters
        for wl in these_greens:
            if wl.letter in blacks[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked green and black in the same location",
                    wl,
                )

            if wl.letter in yellows[wl.index]:
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked green and yellow in the same location",
                    wl,
                )

            # A green character could have been previously marked black only if it was also previously colored
            if wl.letter in _flatten(blacks) and (
                wl.letter not in _flatten(yellows) or wl.letter not in greens
            ):
                raise InvalidWordleLetter(
                    f"'{wl.letter.upper()}' marked green but previously marked black",
                    wl,
                )

        # If we made it through all that validation, append these letters to output
        for wl in word:
            if wl.color == "black":
                blacks[wl.index].append(wl.letter)

            elif wl.color == "yellow":
                yellows[wl.index].append(wl.letter)

            elif wl.color == "green":
                greens[wl.index] = wl.letter

    return blacks, yellows, greens
