#!/home/martin/.cache/pypoetry/virtualenvs/rofi-semantic-vY6w7Ty4-py3.10/bin/python
import argparse
import sys

from semantic import compare


def find_desktop_apps(query):
    app_names, app_scores = compare(query)
    app_names, app_scores = app_names[:5], app_scores[:5]

    for n, s in zip(app_names, app_scores):
        print(f'{n} ({s:.2f}%)', file=sys.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Semantic Search Rofi Interface",
        description="Use semantic search to display desktop apps",
    )

    parser.add_argument('query')
    args = parser.parse_args()
    find_desktop_apps(args.query)
