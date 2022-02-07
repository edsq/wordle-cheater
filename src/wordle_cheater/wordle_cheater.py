from english_words import english_words_lower_alpha_set as words

def load_words():
    return {word for word in words if len(word) == 5}
