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
    word,
    blacks=None,
    yellows=None,
    greens=None,
    counts=None,
    hard=True,
    check_dict=True,
):
    """Check if `word` is a possible solution given previous guesses.

    All inputs must be lowercase as we don't bother to cast them to lowercase to save a bit of time.

    Positional arguments
    -------------------
    word : length-5 string
        The word to check.

    Keyword arguments
    ----------------
    blacks : length-5 list of lists
        A list of lowercase letters that are not in the word.  For example, if our
        guesses have the letter 'A' marked black at the second character,
        `blacks = [[], ['A'], [], [], []]`.
    yellows : length-5 list of lists
        Lowercase letters that are in the word, but not in the correct location.  For example, if
        our guesses tell us that the letter 'A' was in the word, but it was not the third letter, we
        would pass `yellows = [[], [], ['a'], [], []]`.
    greens : length-5 list
        Lowercase letters that are in the word and in the correct location.  For example, if our
        guesses tell us that the letter 'A' is the fourth letter of the word, we would pass
        `greens = [None, None, None, 'a', None]`.
    counts : dict
        Counts of letters that should appear in the solution.  For letters that are in
        `blacks`, this is interpreted as the exact number of times the letter must
        appear in the solution, and defaults to zero.  For letters that are in
        `yellows` and/or `greens`, this is interpreted as the minimum number of times
        the letter must appear in the solution, and defaults to one.
        For example, if a previous guess was 'array' with the two 'r's colored, then we
        would know the solution must have at least two 'r's and pass `counts = {'r': 2}`.
        If a previous guess was 'array', with one 'r' marked black and one colored, then
        we know the solution must have exactly one 'r' and pass `counts = {'r': 1}`.
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
        blacks = [[], [], [], [], []]

    if yellows is None:
        yellows = [[], [], [], [], []]

    if greens is None:
        greens = [None, None, None, None, None]

    if counts is None:
        counts = dict()

    assert len(blacks) == 5
    assert len(yellows) == 5
    assert len(greens) == 5

    # Get unraveled lists
    all_blacks = _flatten(blacks)
    all_yellows = _flatten(yellows)

    # Check for hard mode compliance
    if hard:
        known_letters = all_yellows + [l for l in greens if l is not None]
        for known_letter in known_letters:
            if known_letter not in word:
                return False

            # Also check that there are enough repetitions if applicable
            elif word.count(known_letter) < counts.get(known_letter, 1):
                return False

    # Now check each letter for compatibility with known information
    for i, letter in enumerate(word):
        if letter in all_blacks:
            # If a letter appears as black in the previous guesses, we know how many
            # of that letter we must have - check that here.
            n_of_letter_max = counts.get(letter, 0)
            n_of_letter_in_word = word.count(letter)

            if n_of_letter_in_word > n_of_letter_max:
                return False

        if letter in blacks[i]:
            return False

        elif letter in yellows[i]:
            return False

        elif letter != greens[i] and greens[i] is not None:
            return False

    # Check if guess is a real word
    if check_dict:
        if word not in wordle_words:
            return False

    # If we've made it this far, the word is a possible solution
    return True


def find_words(blacks=None, yellows=None, greens=None, counts=None):
    """Find all possible words that are consistent with current information.

    Keyword arguments
    ----------------
    blacks : length-5 list of lists
        A list of lowercase letters that are not in the word.  For example, if our
        guesses have the letter 'A' marked black at the second character,
        `blacks = [[], ['A'], [], [], []]`.
    yellows : length-5 list of lists
        Lowercase letters that are in the word, but not in the correct location.  For example, if
        our guesses tell us that the letter 'A' was in the word, but it was not the third letter, we
        would pass `yellows = [[], [], ['a'], [], []]`.
    greens : length-5 list
        Lowercase letters that are in the word and in the correct location.  For example, if our
        guesses tell us that the letter 'A' is the fourth letter of the word, we would pass
        `greens = [None, None, None, 'a', None]`.
    counts : dict
        Counts of letters that should appear in the solution.  For letters that are in
        `blacks`, this is interpreted as the exact number of times the letter must
        appear in the solution, and defaults to zero.  For letters that are in
        `yellows` and/or `greens`, this is interpreted as the minimum number of times
        the letter must appear in the solution, and defaults to one.
        For example, if a previous guess was 'array' with the two 'r's colored, then we
        would know the solution must have at least two 'r's and pass `counts = {'r': 2}`.
        If a previous guess was 'array', with one 'r' marked black and one colored, then
        we know the solution must have exactly one 'r' and pass `counts = {'r': 1}`.

    Returns
    -------
    possible_words : list
        List of possible solutions that match the given guesses.
    """
    possible_words = []
    for word in wordle_words:
        if check_word(
            word,
            blacks=blacks,
            yellows=yellows,
            greens=greens,
            counts=counts,
            hard=True,
        ):
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
        `blacks = [[], ['A'], [], [], []]`.
    yellows : length-5 list of lists
        Lowercase letters that are in the word, but not in the correct location.  For
        example, if our guesses tell us that the letter 'A' was in the word, but it was
        not the third letter, `yellows = [[], [], ['a'], [], []]`.
    greens : length-5 list
        Lowercase letters that are in the word and in the correct location.  For
        example, if our guesses tell us that the letter 'A' is the fourth letter of the
        word, `greens = [None, None, None, 'a', None]`.
    counts : dict
        Counts of letters that should appear in the solution.  For letters that are in
        `blacks`, this is interpreted as the exact number of times the letter must
        appear in the solution, and defaults to zero.  For letters that are in
        `yellows` and/or `greens`, this is interpreted as the minimum number of times
        the letter must appear in the solution, and defaults to one.
        For example, if a previous guess was 'array' with the two 'r's colored, then we
        would know the solution must have at least two 'r's and so `counts = {'r': 2}`.
        If a previous guess was 'array', with one 'r' marked black and one colored, then
        we know the solution must have exactly one 'r' and so `counts = {'r': 1}`.
    """

    blacks = [[], [], [], [], []]
    yellows = [[], [], [], [], []]
    greens = [None, None, None, None, None]
    counts = dict()

    if len(wordle_letters) % 5 != 0:
        raise ValueError("`len(wordle_letters)` must be an integer multiple of five")

    words = [wordle_letters[i * 5 : i * 5 + 5] for i in range(len(wordle_letters) // 5)]

    for word in words:
        these_blacks = [wl for wl in word if wl.color == "black"]
        these_yellows = [wl for wl in word if wl.color == "yellow"]
        these_greens = [wl for wl in word if wl.color == "green"]

        these_counts = dict()
        for wl in these_yellows + these_greens:
            these_counts[wl.letter] = these_counts.get(wl.letter, 0) + 1

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

            # A black character cannot be colored in this word fewer times than in any
            # previous word
            curr_count = these_counts.get(wl.letter, 0)
            prev_count = counts.get(wl.letter, 0)
            if curr_count < prev_count:
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
            if wl.letter in _flatten(blacks) and counts.get(wl.letter, 0) == 0:
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
            if wl.letter in _flatten(blacks) and counts.get(wl.letter, 0) == 0:
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

            # Also update counts if necessary
            # If not playing hard mode, the current count of a letter could be less
            # than the final count, so only update count if it has increased
            if these_counts.get(wl.letter, 0) > counts.get(wl.letter, 0):
                counts[wl.letter] = these_counts[wl.letter]

    return blacks, yellows, greens, counts
