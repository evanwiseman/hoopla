#!/usr/bin/env python3

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from movies import load_movies, query_movies, print_movies

FP_MOVIES = "./data/movies.json"


class Args:
    command: str
    query: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args(namespace=Args)

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            movies = load_movies(FP_MOVIES)
            queried_movies = query_movies(args.query, movies)
            print_movies(queried_movies, 5)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
