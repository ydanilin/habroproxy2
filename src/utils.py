"""
    Most important part here is multi_insert() function for interceptor
    (see TMInterceptor in interceptors.py and project readme for details)
"""
from itertools import zip_longest, chain
from time import localtime, strftime


def get_time():
    """
        Returns string representation of computer's time
        Used for server logging, shows info without date
    """
    return strftime("%H:%M:%S", localtime())


def str_has_digits(stream):
    """ to check if a word has digits inside """
    return any(map(lambda x: x.isdigit(), stream))


def insert_if_needed(what, cond_len):
    """
        Returns function to be used in map()
        Appends <what> to the end of a word if word length is <cond_len>
    """
    # pylint: disable=line-too-long
    return lambda word: f'{word}{what}' if len(word) == cond_len and not str_has_digits(word) else word


def multi_insert(stri, what, cond_len, special):
    """
        Inserts <what> at the end of every word in the <stri> if
        the length of this word is <cond_len> characters.
        Which symbols will be used as separators defined in <special> string.
        Example is in test_utils.py
    """
    word = ''
    words = []
    separ = ''
    separs = []
    # peek into the string to set start state
    state = 'inside' if stri[0] not in special else 'outside'
    initial_state = state
    for char in stri:
        if state == 'inside':
            if char not in special:
                word += char
            else:
                separ += char
                words.append(word)
                word = ''
                state = 'outside'
        elif state == 'outside':
            if char in special:
                separ += char
            else:
                word += char
                separs.append(separ)
                separ = ''
                state = 'inside'
    # inclusion of last accumulator variable (word or separ) after cycle complete
    if state == 'inside':
        words.append(word)
    elif state == 'outside':
        separs.append(separ)
    # modification
    modified_words = map(insert_if_needed(what, cond_len), words)
    zip_back = (modified_words, separs) if initial_state == 'inside' else (separs, modified_words)
    reconstructed = chain(*zip_longest(*zip_back, fillvalue=''))
    return ''.join(reconstructed)
