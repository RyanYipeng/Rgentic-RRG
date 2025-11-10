from typing import List
from qdrant_client.models import PointStruct
from .data import ML_FAQ, EmbedData
from .vdb import QdrantVDB


class Retriever:
    def __init__(self, vdb: QdrantVDB, embed: EmbedData):
        self.vdb = vdb
        self.embed = embed
        self._seed()

    def _seed(self):
        # Turn Q/A into a single text for semantic search
        texts = [f"Q: {row['q']}\nA: {row['a']}" for row in ML_FAQ]
        vectors = self.embed.encode(texts)
        points = [
            PointStruct(id=row["id"], vector=vectors[i], payload=row)
            for i, row in enumerate(ML_FAQ)
        ]
        self.vdb.upsert(points)

    def search(self, query: str, k: int = 3) -> str:
        vec = self.embed.encode(query)
        hits = self.vdb.search(vec, limit=k)
        formatted = []
        for h in hits:
            p = h.payload
            formatted.append(f"Q: {p['q']}\nA: {p['a']}\n(score={h.score:.4f})")
        return "\n\n".join(formatted)
