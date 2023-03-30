""" Class for encoding strings into query strings

SemanticTransformer is a singleton class holding a model that will encode an array of string.

Typical usage example:

    model = SemanticTransformer()
    embeddings = model.encode(string)
"""
from sentence_transformers import SentenceTransformer
from abc import ABC, abstractmethod

from constants import TRANSFORMER_URL


class SingletonClass(ABC):
    """A singleton class used as a parent for semantic embedding fo strings.

    Attributes:
        __instance: Private attr that holds the class itself to check whether it has already been created.
    """
    __instance = None

    def __new__(cls):
        """Create class only once.

        Args:
            cls: class instance

        Returns:
            The single instantiation of that classs.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @abstractmethod
    def encode(self, queries):
        """ General Method that encodes an array of strings into a latent space.

        Args:
            queries: An array of strings to be encoded.

        Returns:
            An array of the same size as the queries where each element holds the latent space embedding
            of said string.
        """
        raise NotImplementedError


class SemanticTransformer(SingletonClass):
    """Singleton transformer to embed strings into latent space.

    Attributes:
        __model: SentenceTransformer for encoding strings into latent space.
        __model_url: url to a huggingsface sentence_tranformer.
    """
    __model = None

    def __init__(self):
        """Only use one instance of class and add a model if it hasn't been added.
        """
        if self.__model is None:
            self.__model = SentenceTransformer(TRANSFORMER_URL)

    def encode(self, queries):
        """Use sentence transformer to embed strings into latent space.

        Args:
            queries: An array of strings to be encoded.

        Returns:
            An array of the same size as the queries where each element holds the latent space embedding
            of said string.

        """
        embeddings = self.__model.encode(queries)
        return embeddings
