import string
from nltk.stem import PorterStemmer

FP_STOPWORDS = "./data/stopwords.txt"
_stemmer: PorterStemmer | None = None  # cache
_stopwords: list | None = None  # cache


def clean_text(text: str) -> str:
    # Convert to lower
    text = text.lower()

    # Remove punctuation
    translation_table = str.maketrans("", "", string.punctuation)
    return text.translate(translation_table)


def tokenize(text: str) -> list[str]:
    tokens = text.split(" ")
    return tokens


def reduce_stem(tokens: list[str]) -> list[str]:
    global _stemmer
    if _stemmer is None:
        _stemmer = PorterStemmer()

    stemmed = list(map(lambda token: _stemmer.stem(token), tokens))
    return stemmed


def get_stopwords() -> set[str]:
    global _stopwords
    if _stopwords is not None:
        return _stopwords

    with open(FP_STOPWORDS, encoding="utf-8") as f:
        text = f.read()
        _stopwords = set(text.splitlines())
    return _stopwords


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopwords = get_stopwords()  # faster membership checks
    return [t for t in tokens if t.lower() not in stopwords]
