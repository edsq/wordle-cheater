"""Utilities for generating solutions to Wordle given previous guesses."""
from dataclasses import dataclass

from wordle_cheater.dictionary import letters, wordle_dictionary


class InvalidWordleLetters(Exception):
    """Exception for when invalid letters are passed to WordleGuesses.

    Attributes
    ----------
    invalid_letters : list of WordleLetter objects
        The relevant letters that were found to be invalid given previously entered
        guesses.
    """

    def __init__(self, message, wordle_letters):
        self.invalid_letters = wordle_letters
        super().__init__(message)


@dataclass
class WordleLetter:
    """Class describing a single letter in a Wordle guess.

    Parameters
    ----------
    letter : str
        The letter in question.  Should be lower case.
    color : {"black", "yellow", "green"}
        The color Wordle marked the letter.
    index : {0, 1, 2, 3, 4}
        The location in the word where the letter appeared.
    """

    letter: str
    color: str
    index: int

    def __post_init__(self):
        """Do parameter validation."""
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

    def __lt__(self, other):
        """Deterimine if `self` is less than `other`.

        Sorts by index.

        Parameters
        ----------
        other : WordleLetter
            The other WordleLetter to compare against.

        Returns
        -------
        bool
            Whether `self.index` is less than `other.index`.
        """
        return self.index < other.index


class WordleGuesses:
    """Class representing all current guesses and their colors.

    Parameters
    ----------
    wordle_letters : list of WordleLetters, optional
        The initial words to add.  Length must be an integer multiple of five.

    Attributes
    ----------
    wordle_letters : list of WordleLetters
        All the letters that have been entered so far.
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

    def __init__(self, wordle_letters=None):
        if wordle_letters is None:
            wordle_letters = []

        self.wordle_letters = wordle_letters.copy()
        self.blacks = [[], [], [], [], []]
        self.yellows = [[], [], [], [], []]
        self.greens = [None, None, None, None, None]
        self.counts = dict()

        if len(wordle_letters) % 5 != 0:
            raise ValueError(
                "`len(wordle_letters)` must be an integer multiple of five"
            )

        words = [
            wordle_letters[i * 5 : i * 5 + 5] for i in range(len(wordle_letters) // 5)
        ]

        for word in words:
            self.add_word(word)

    def add_word(self, word):
        """Update current guesses.

        This method appends to `self.wordle_letters` and updates `self.blacks`,
        `self.yellows`, `self.greens`, and `self.counts`.

        Parameters
        ----------
        word : length-5 list of WordleLetters
            The word to add to the current guesses.

        Raises
        ------
        InvalidWordleLetters
            If `word` contains WordleLetters that are impossible given previous guesses.
        """
        if len(word) != 5 or any([not isinstance(wl, WordleLetter) for wl in word]):
            raise ValueError("`word` must be a length-5 list of WordleLetter objects.")

        # Get any invalid letters in the word
        invalid_letters = self.get_invalid_letters(word)

        # Raise an error, if necessary
        if len(invalid_letters) > 0:
            invalid_letters = sorted(invalid_letters)  # Sort by index
            letters_str = ", ".join([wl.letter.upper() for wl in invalid_letters])
            inds_str = ", ".join([str(wl.index) for wl in invalid_letters])
            exc_str = (
                "Letters "
                + letters_str
                + " (indices "
                + inds_str
                + ") incompatible with previous guesses"
            )
            raise InvalidWordleLetters(exc_str, invalid_letters)

        # If we made it this far, update current list of letters
        self.wordle_letters += word

        # Add the word to self.blacks, self.yellows, self.greens, self.counts
        these_counts = dict()  # colored letters in this word and their counts
        for wl in word:
            if wl.color == "black":
                self.blacks[wl.index].append(wl.letter)

            elif wl.color == "yellow":
                self.yellows[wl.index].append(wl.letter)
                these_counts[wl.letter] = these_counts.get(wl.letter, 0) + 1

            else:  # Color is green
                self.greens[wl.index] = wl.letter
                these_counts[wl.letter] = these_counts.get(wl.letter, 0) + 1

            # Also update counts if necessary
            # If not playing hard mode, the current count of a letter could be less
            # than the final count, so only update count if it has increased
            if these_counts.get(wl.letter, 0) > self.counts.get(wl.letter, 0):
                self.counts[wl.letter] = these_counts[wl.letter]

    def get_invalid_letters(self, word):
        """Get which of letters in `word` (if any) are invalid given current guesses.

        Parameters
        ----------
        word : length-5 list of WordleLetters
            The word to check.

        Returns
        -------
        list of WordleLetters
            The invalid letters of `wordle_letters`, an empty list if there were none.
        """
        if len(word) != 5:
            raise ValueError("`word` must be a length-5 list of WordleLetter objects.")

        these_blacks = [wl for wl in word if wl.color == "black"]
        these_yellows = [wl for wl in word if wl.color == "yellow"]
        these_greens = [wl for wl in word if wl.color == "green"]

        # Get the counts of colored letters in this word
        these_counts = dict()
        for wl in these_yellows + these_greens:
            these_counts[wl.letter] = these_counts.get(wl.letter, 0) + 1

        invalid_letters = []  # For letters incompatible with previous words

        # Validate black letters
        for wl in these_blacks:
            # A black letter cannot be colored in this word fewer times than in any
            # previous word, and can't have been previously marked colored at this
            # location
            curr_count = these_counts.get(wl.letter, 0)
            prev_count = self.counts.get(wl.letter, 0)
            if (
                curr_count < prev_count
                or wl.letter in self.yellows[wl.index]
                or wl.letter == self.greens[wl.index]
            ):
                invalid_letters.append(wl)

        # Validate yellow letters
        for wl in these_yellows:
            # A yellow letter can't have been previously marked black or green in
            # this location, and if it was previously marked black (anywhere), it must
            # have also been previously colored
            if (
                wl.letter in self.blacks[wl.index]
                or wl.letter == self.greens[wl.index]
                or wl.letter in _flatten(self.blacks)
                and self.counts.get(wl.letter, 0) == 0
            ):
                invalid_letters.append(wl)

        # Validate green letters
        for wl in these_greens:
            # A green letter can't have been previously marked black or yellow in
            # this location, a different letter can't have been marked green in this
            # location, and if it was previously marked black (anywhere), it must have
            # also been previously colored
            if (
                wl.letter in self.blacks[wl.index]
                or wl.letter in self.yellows[wl.index]
                or wl.letter != self.greens[wl.index]
                and self.greens[wl.index] is not None
                or wl.letter in _flatten(self.blacks)
                and self.counts.get(wl.letter, 0) == 0
            ):
                invalid_letters.append(wl)

        return invalid_letters


def _flatten(list_):
    """Flatten a list of lists into a 1D list."""
    return [item for sublist in list_ for item in sublist]


def check_word(word, guesses, check_dict=True):
    """Check if `word` is a possible solution given previous guesses.

    All inputs must be lowercase as we don't bother to cast them to lowercase to save a
    bit of time.

    Parameters
    ----------
    word : length-5 string
        The word to check.
    guesses : WordleGuesses
        The previous guesses to check against.
    check_dict : bool, optional
        Whether or not to check if `word` is a real five letter english word.

    Returns
    -------
    valid : bool
        Whether or not `word` is a possible solution given `blacks`, `yellows`, and
        `greens`.
    """
    blacks = guesses.blacks
    yellows = guesses.yellows
    greens = guesses.greens
    counts = guesses.counts

    # Get unraveled lists
    all_blacks = _flatten(blacks)
    all_yellows = _flatten(yellows)

    # Check for "hard mode compliance"
    known_letters = all_yellows + [l_ for l_ in greens if l_ is not None]
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

        # Letter can't have been previously colored black or yellow at this index
        if letter in blacks[i] or letter in yellows[i]:
            return False

        # A different letter can't have been previously colored green at this index
        elif letter != greens[i] and greens[i] is not None:
            return False

    # Check if guess is a real word
    if check_dict and word not in wordle_dictionary:
        return False

    # If we've made it this far, the word is a possible solution
    return True


def find_words(guesses):
    """Find all possible words that are consistent with `guesses`.

    Parameters
    ----------
    guesses : WordleGuesses
        The guesses to check against.

    Returns
    -------
    possible_words : list
        List of possible solutions that match the given guesses.
    """
    possible_words = []
    for word in wordle_dictionary:
        if check_word(word, guesses):
            possible_words.append(word)

    return possible_words


def cheat(wordle_letters):
    """Given a list of WordleLetter objects, return possible solutions.

    Parameters
    ----------
    wordle_letters : list of WordleLetter
        The previous guesses.  Every five WordleLetters are interpreted as one word.

    Returns
    -------
    possible_words : list of str
        A list of the possible solutions given `wordle_letters`, in random order.
    """
    guesses = WordleGuesses(wordle_letters)
    possible_words = find_words(guesses)
    return possible_words


def get_wordle_letters(letters, colors):
    """Create a list of WordleLetter objects.

    Parameters
    ----------
    letters : str
        The previous guesses.  Whitespace will be ignored.
    colors : str
        The colors corresponding to each letter.  Each character in this string must
        be one of 'b', 'y', or 'g', which correspond to 'black', 'yellow', or 'green',
        respectively.  Whitespace will be ignored.

    Returns
    -------
    wordle_letters : list of WordleLetter
        The WordleLetter objects corresponding to the input letters and colors.
    """
    # Remove whitespace
    letters = "".join(letters.split())
    colors = "".join(colors.split())

    # Make lower case
    letters = letters.lower()
    colors = colors.lower()

    # Create WordleLetter objects
    wordle_letters = []
    for i, (l, c) in enumerate(zip(letters, colors)):
        if c == "b":
            color = "black"

        elif c == "y":
            color = "yellow"

        elif c == "g":
            color = "green"

        else:
            raise ValueError(f"`colors` must contain only 'b', 'y', or 'g' (got {c}).")

        wordle_letters.append(WordleLetter(letter=l, color=color, index=i % 5))

    return wordle_letters


def easy_cheat(letters, colors):
    """Given previous guesses on Wordle, return a list of possible solutions.

    Parameters
    ----------
    letters : str
        The previous guesses.  Whitespace will be ignored.
    colors : str
        The colors corresponding to each letter.  Each character in this string must
        be one of 'b', 'y', or 'g', which correspond to 'black', 'yellow', or 'green',
        respectively.  Whitespace will be ignored.

    Returns
    -------
    possible_words : list of str
        A list of the possible solutions in random order.
    """
    wordle_letters = get_wordle_letters(letters, colors)
    possible_words = cheat(wordle_letters)
    return possible_words
