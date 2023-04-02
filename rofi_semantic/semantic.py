from os import path

import numpy as np

import os
import argparse
import json

from scipy.special import softmax

from semantic_transformer import SemanticTransformer
from constants import EMBEDDINGS_PATH
from app_information import get_app_information


def get_app_embeddings():
    """Find the latent embeddings of the applications.

    Check first for a saved copy of the embeddings. If it doesn't exist, create them
    and save a copy.

    Returns:
        A tuple of np.arrays with the same first dimension.
        The first array in the tuple holds the names off the listed apps.
        The second array in the tuple holds the latent space embedded apps.
    """
    if path.isfile(EMBEDDINGS_PATH):
        try:
            with open(EMBEDDINGS_PATH, 'r') as f:
                app_info = json.load(f)
        except (json.JSONDecodeError):
            os.remove(EMBEDDINGS_PATH)
            get_app_embeddings
    else:
        app_info = get_app_information()
        with open(EMBEDDINGS_PATH, 'w') as f:
            json.dump(app_info, f)

    return app_info


def compare(querystring):
    """Compare the querystring to the apps in latent space.

    Args:
        querystring: A single string that will be encoded into a latent space
    """
    app_info = get_app_embeddings()

    # Compute distance and normalize/standartize
    query_embedding = SemanticTransformer().encode([querystring])
    distances = np.linalg.norm(app_latent - query_embedding, axis=1)
    distances = -(distances - distances.mean()) / distances.std()
    percentage_score = softmax(distances) * 100

    # Sort
    sort_index = np.argsort(percentage_score)[::-1]
    app_names = app_names[sort_index]
    scores = percentage_score[sort_index]

    return app_names, scores


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

    names, scores = compare(args.querystring)
    for name, score in list(zip(names, scores))[0:10]:
        print(f'{name}: {score}')
