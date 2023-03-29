from os import path

import numpy as np

import os
import argparse
import subprocess
import json

from semantic_transformer import SemanticTransformer

EMBEDDINGS_PATH = './desktop_embeddings.json'
APPLICATION_PATH = '/usr/share/applications/'


def list_apps():
    """List desktop apps in the APPLICATION_PATH folder.

    :return: array with desktop app names
    """
    command = 'ls ' + APPLICATION_PATH
    ls_output = subprocess.check_output(command, shell=True)

    program_list = ls_output.decode().split('\n')

    # remove desktop postfix
    program_list = [app_basename.replace('.desktop', '') for app_basename in program_list]
    return program_list


def get_app_embeddings():
    """Find the latent embeddings of the applications.

    Check first for a saved copy of the embeddings. If it doesn't exist, create them
    and save a copy

    :return: latent embedding of desktop apps
    """
    if path.isfile(EMBEDDINGS_PATH):
        try:
            with open(EMBEDDINGS_PATH, 'r') as f:
                embeddings = json.load(f)
        except (json.JSONDecodeError):
            os.remove(EMBEDDINGS_PATH)
            get_app_embeddings
    else:
        apps = list_apps()
        embeddings = SemanticTransformer().encode(apps)
        embeddings = [[app, emb.tolist()] for app, emb in list(zip(apps, embeddings))]

        with open(EMBEDDINGS_PATH, 'w') as f:
            json.dump(embeddings, f)

    app_names = np.array([a for a, _ in embeddings])
    app_latent = np.array([e for _, e in embeddings])

    return app_names, app_latent


def square(x):
    return x ** 2


def compare(querystring):
    app_names, app_latent = get_app_embeddings()

    # Compute Scores
    query_embedding = SemanticTransformer().encode([querystring])
    scores = np.dot(app_latent, np.transpose(query_embedding))
    scores = square(scores.flatten())

    # Sort
    sort_index = np.argsort(scores)[::-1]
    app_names = app_names[sort_index]
    scores = scores[sort_index]

    app_scores = list(zip(app_names, scores))

    return app_scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Semantic App Search",
        description="Use the latent space of transformer to find the semantically closest desktop app."
    )
    parser.add_argument(
        '-q', '--querystring',
        required=True,
        type=str,
        help="The query looking for the appropriate app. For example 'video editing kde'"
    )
    args = parser.parse_args()

    scored = compare(args.querystring)
    for name, score in scored[0:10]:
        print(f'{name}: {score}')

