import os
from openai import OpenAI
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers.SentenceTransformer import SentenceTransformer

from services.embeddings_service import EmbeddingsService

load_dotenv()

def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=os.environ.get("QDRANT_BASE_URL"),
                        port=os.environ.get("QDRANT_PORT"))
    
def get_embeddings_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")

async def get_embeddings_service(client = get_qdrant_client()) -> EmbeddingsService:
    embeddings = get_embeddings_model()
    return EmbeddingsService(embeddings=embeddings, vector_db=client)
