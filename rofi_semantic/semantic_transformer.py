from sentence_transformers import SentenceTransformer


class SemanticTransformer:
    __instance = None
    __model = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SemanticTransformer, cls).__new__(cls)
            cls.__model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        return cls.__instance

    def encode(self, queries):
        embeddings = self.__model.encode(queries)
        return embeddings

