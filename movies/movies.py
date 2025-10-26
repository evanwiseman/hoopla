import json


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
    for movie in movies:
        if query in movie.get_title():
            result.append(movie)
    return result


def print_movies(movies: list[Movie], n: int) -> None:
    for i, movie in enumerate(movies):
        if i >= n:
            break
        print(f"{i + 1}. {movie.get_title()}")
