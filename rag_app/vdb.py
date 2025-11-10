from typing import Iterable
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantVDB:
    """Thin wrapper around Qdrant for this demo.

    By default uses an in-memory Qdrant instance (no external service needed).
    To use a running Qdrant server instead, pass `url` (and optional `api_key`).
    """
    def __init__(self, collection: str, vector_size: int, url: str | None = None, api_key: str | None = None):
        if url:
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            # Embedded/in-memory Qdrant
            self.client = QdrantClient(path=":memory:")
        self.collection = collection
        self.vector_size = vector_size
        self._ensure_collection()

    def _ensure_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
        )

    def upsert(self, points: Iterable[PointStruct]):
        self.client.upsert(collection_name=self.collection, points=list(points))

    def search(self, vector: list[float], limit: int = 3):
        return self.client.search(collection_name=self.collection, query_vector=vector, limit=limit)
