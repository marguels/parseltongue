from pathlib import Path
import os
from typing import List
from dotenv import load_dotenv
from qdrant_client import models, QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import SentenceTransformer

from langchain_text_splitters import MarkdownTextSplitter

from models.search_response_model import SearchResponseModel

load_dotenv()

class EmbeddingsService:
    def __init__(self, embeddings: SentenceTransformer, vector_db: QdrantClient):
        self.embeddings = embeddings
        self.vector_db = vector_db
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")
        self.initialize_collection()
        
    def initialize_collection(self):
        """Method to initialize Qdrant collection"""
        try:
            self.vector_db.get_collection(self.collection_name)
        except UnexpectedResponse as e:
            if "doesn't exist" in str(e):
                print(f"Collection {self.collection_name} not found. Creating it. Error: {str(e)}")
                self.vector_db.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                    size=self.embeddings.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE,
                    )
                )
                self.upload_documents()
            else:
                raise e

    def search_documents(self, query: str) -> List[SearchResponseModel]:
        """Method to search documents by query"""
        if not query:
            raise ValueError('Please specify a query')

        hits = self.vector_db.search(
            collection_name=self.collection_name,
            query_vector=self.embeddings.encode(query).tolist(),
            limit=3,
        )

        return [hit.payload for hit in hits]

    def upload_documents(self):
        """Method to upload documents to the Qdrant collection"""
        document_data = self.chunk_all_documents_in_path()
        self.vector_db.upload_points(collection_name=self.collection_name,
                     points=[
                        models.PointStruct(
                           id=idx,
                           vector=self.embeddings.encode(doc["content"]).tolist(),
                           payload=doc
                        )
                        for idx, doc in enumerate(document_data)
                    ],
                )

    def chunk_all_documents_in_path(self, ps: list = None) -> list[dict[str, str]]:
        """Method to pre-process and chunk all documents in specified path."""
        if ps is None:
            ps = list(Path(os.getenv("OBSIDIAN_VAULT_PATH")).glob("**/*.md"))
        documents_paths = [
            path for path in ps
            if '.obsidian' not in path.parts
            and not any(part.startswith('_') for part in path.parts)
            and path.name != "1 - ARTICLES KANBAN.md"
        ]
        data = []
        sources = []
        for p in documents_paths:
            data.append(self.get_document(p))
            sources.append(p.name)

        docs = []
        metadatas = []
        for i, d in enumerate(data):
            splits = self.chunk_document(d)
            docs.extend(splits)
            metadatas.extend([sources[i]] * len(splits))

        return [{"source": metadatas[i], "content": docs[i]} for i in range(len(docs))]

    def chunk_document(self, content: str) -> list[str]:
        """Method to chunk documents"""
        text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=20)
        return text_splitter.split_text(content)


    def get_document(self, full_path: str) -> str:
        """
        Util method to fetch document at a specified path.
        """
        try:
            with open(full_path) as f:
                return f.read()
        except FileNotFoundError:
            print(f"File {full_path} not found.")
