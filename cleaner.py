import re
from string import punctuation

import Stemmer


def glue_fields(dict_, fileds):
    result = ""
    for field in fileds:
        result += _prepare_field(dict_[field]) + " "

    return _stem_words(result.split())


def _prepare_field(value):
    return _remove_punctuation(
        _remove_noise_words(
            _remove_tags(
                value
            )
        )
    )

def _remove_tags(value):
    return re.sub(
        re.compile("<.*?>"),
        " ",
        value
    )

def _remove_noise_words(value):
    with open("noise_words.txt", "r") as f:
        noise_words = [line.strip() for line in f]

    return ' '.join(c for c in value.split() if c not in noise_words)

def _remove_punctuation(value):
    return ''.join(c for c in value if c not in punctuation)

def _stem_words(words):
    return " ".join(
        Stemmer.Stemmer('russian').stemWords(words)
    )
