import string


def clean_text(text: str) -> str:
    # Convert to lower
    text = text.lower()

    # Remove punctuation
    translation_table = str.maketrans("", "", string.punctuation)
    return text.translate(translation_table)


def tokenize(text: str) -> list[str]:
    tokens = text.split(" ")
    return tokens
