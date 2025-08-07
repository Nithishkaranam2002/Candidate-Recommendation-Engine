from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def get_embedding(text):
    return model.encode([text])[0]
