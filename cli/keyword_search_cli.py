#!/usr/bin/env python3

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from libs import load_movies, InvertedIndex, tokenize, clean_text

FP_MOVIES = "./data/movies.json"


class Args:
    command: str
    query: str
    doc_id: int
    term: str


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Builds an inverted index tree")  # noqa: F841

    tf_parser = subparsers.add_parser("tf", help="Get the term frequency given an id")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Search term")

    args = parser.parse_args(namespace=Args)
    tree = InvertedIndex()
    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            try:
                tree.load()
            except FileNotFoundError:
                print("missing inverted index tree: use build")
                sys.exit(1)

            tokens = tokenize(clean_text(args.query))
            ids = []
            for token in tokens:
                movie_ids = tree.get_document_ids(token)
                ids.extend(movie_ids)
            ids.sort()
            for i in range(min(5, len(ids))):
                movie = tree.docmap[ids[i]]
                print(ids[i], movie.get_title())
        case "build":
            print("Building inverted index tree")
            movie_ids = load_movies(FP_MOVIES)
            tree.build(movie_ids)
            tree.save()
        case "tf":
            try:
                tree.load()
            except FileNotFoundError:
                print("missing inverted index tree: use build")
                sys.exit(1)

            frequency = tree.get_tf(
                args.doc_id,
                args.term,
            )
            print(f"{args.doc_id} {args.term} appears {frequency} times")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
