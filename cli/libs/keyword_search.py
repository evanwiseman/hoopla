import json
import pickle
import os
from collections import defaultdict, Counter
from .search_utils import clean_text, tokenize, remove_stopwords, reduce_stem


class Document:
    def __init__(self, id: int, title: str, description: str) -> None:
        self._id = id
        self._title = title
        self._description = description

    def get_id(self) -> int:
        return self._id

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description


def load_movies(fp: str) -> list[Document]:
    try:
        with open(fp) as f:
            data = json.load(f)
        return [Document(**d) for d in data["movies"]]

    except Exception as e:
        print(f"error loading movies: {e}")
        return []


def query_movies(query: str, movies: list[Document]) -> list[Document]:
    result = []
    clean_query = clean_text(query)

    query_tokens = reduce_stem(remove_stopwords(tokenize(clean_query)))
    for movie in movies:
        # clean the text
        clean_title = clean_text(movie.get_title())

        # resolve into tokens
        title_tokens = reduce_stem(remove_stopwords(tokenize(clean_title)))

        num_matching = 0  # number of matching tokens
        for query_token in query_tokens:
            for movie_title_token in title_tokens:
                if query_token in movie_title_token:
                    num_matching += 1

        # append to results if 1 or more is matching
        if num_matching >= 1:
            result.append(movie)
    return result


def print_movies(movies: list[Document], n: int) -> None:
    for i, movie in enumerate(movies):
        if i >= n:
            break
        print(f"{i + 1}. {movie.get_title()}")


class InvertedIndex:
    index: dict[str, set[int]] = defaultdict(set[int])
    docmap: dict[int, Document] = {}
    term_frequencies: dict[int, Counter] = defaultdict(Counter)

    def __add_document(self, doc_id: int, text: str) -> None:
        tokens = reduce_stem(remove_stopwords(tokenize(clean_text(text))))
        self.term_frequencies[doc_id] = Counter(tokens)
        for token in tokens:
            self.index[token].add(doc_id)

    def get_document_ids(self, term: str) -> list[int]:
        ids = self.index.get(clean_text(term))
        if not ids:
            return []

        return sorted(list(ids))

    def get_tf(self, doc_id: int, term: str) -> int:
        return self.term_frequencies.get(doc_id, {}).get(term, 0)

    def build(self, movies: list[Document]):
        for movie in movies:
            self.__add_document(
                movie.get_id(),
                f"{movie.get_title()} {movie.get_description()}",
            )
            self.docmap[movie.get_id()] = movie

    def save(self):
        os.makedirs("cache", exist_ok=True)
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)
        with open("cache/term_frequencies", "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def load(self):
        with open("cache/index.pkl", "rb") as f:
            self.index = pickle.load(f)
        with open("cache/docmap.pkl", "rb") as f:
            self.docmap = pickle.load(f)
        with open("cache/term_frequencies", "rb") as f:
            self.term_frequencies = pickle.load(f)
