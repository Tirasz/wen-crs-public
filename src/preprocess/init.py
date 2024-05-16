from configs import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer

sentences = ["This is a dummy sentence"]
model = SentenceTransformer(EMBEDDING_MODEL)
model.encode(sentences)
