""" Class for encoding strings into query strings

SemanticTransformer is a singleton class holding a model that will encode an array of string.

Typical usage example:

    model = SemanticTransformer()
    embeddings = model.encode(string)
"""
from sentence_transformers import SentenceTransformer


class SingletonClass:
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
            cls.__instance = super(SingletonClass, cls).__new__(cls)
        return cls.__instance

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
    __model_url = 'sentence-transformers/all-MiniLM-L6-v2'

    def __new__(cls):
        """Only use one instance of class and add a model if it hasn't been added.

        Args:
            cls: SemanticTransformer.
        """
        super().__new__(cls)
        if cls.__model is None:
            cls.__model = SentenceTransformer(cls.__model_url)
        return cls.__instance

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
