from nltk.stem import PorterStemmer

_stemmer: PorterStemmer | None = None  # cache


def reduce_stem(tokens: list[str]) -> list[str]:
    global _stemmer
    if _stemmer is None:
        _stemmer = PorterStemmer()

    stemmed = list(map(lambda token: _stemmer.stem(token), tokens))
    return stemmed
