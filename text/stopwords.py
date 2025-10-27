FP_STOPWORDS = "./data/stopwords.txt"

_stopwords: list | None = None  # cache


def get_stopwords() -> list[str]:
    global _stopwords
    if _stopwords is not None:
        return _stopwords

    with open(FP_STOPWORDS, encoding="utf-8") as f:
        text = f.read()
        _stopwords = text.splitlines()
    return _stopwords


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopwords = set(get_stopwords())  # faster membership checks
    return [t for t in tokens if t.lower() not in stopwords]
