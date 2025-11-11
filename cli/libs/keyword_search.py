import json
import pickle
import os
from collections import defaultdict
from .search_utils import clean_text, tokenize, remove_stopwords, reduce_stem


class Movie:
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


def load_movies(fp: str) -> list[Movie]:
    try:
        with open(fp) as f:
            data = json.load(f)
        return [Movie(**m) for m in data["movies"]]

    except Exception as e:
        print(f"error loading movies: {e}")
        return []


def query_movies(query: str, movies: list[Movie]) -> list[Movie]:
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


def print_movies(movies: list[Movie], n: int) -> None:
    for i, movie in enumerate(movies):
        if i >= n:
            break
        print(f"{i + 1}. {movie.get_title()}")


class InvertedIndex:
    index: dict[str, set[int]] = defaultdict(set[int])
    docmap: dict[int, Movie] = {}

    def __add_document(self, doc_id, text) -> None:
        tokens = tokenize(clean_text(text))
        for token in tokens:
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list[int]:
        doc_ids = self.index.get(clean_text(term))
        if not doc_ids:
            return []

        return sorted(list(doc_ids))

    def build(self, movies: list[Movie]):
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
