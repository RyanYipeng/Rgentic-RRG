from dataclasses import dataclass
from typing import List
from sentence_transformers import SentenceTransformer

# Simple embedding wrapper
@dataclass
class EmbedData:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    def __post_init__(self):
        self.model = SentenceTransformer(self.model_name)

    @property
    def dim(self) -> int:
        # get_sentence_embedding_dimension is more robust than accessing .get_sentence_embedding_dimension()
        try:
            return self.model.get_sentence_embedding_dimension()
        except Exception:
            # Fallback: embed a short text to infer dimension
            return len(self.model.encode("dimension probe"))

    def encode(self, texts: List[str] | str) -> list:
        if isinstance(texts, str):
            return self.model.encode(texts).tolist()
        return self.model.encode(texts).tolist()


# A tiny ML FAQ seed dataset for the demo.
ML_FAQ = [
    {
        "id": 1,
        "q": "What is supervised learning?",
        "a": "Supervised learning maps inputs to labeled outputs using example pairs; common tasks include classification and regression."
    },
    {
        "id": 2,
        "q": "What is unsupervised learning?",
        "a": "Unsupervised learning finds structure in unlabeled data, e.g., clustering and dimensionality reduction."
    },
    {
        "id": 3,
        "q": "What is overfitting?",
        "a": "Overfitting happens when a model memorizes the training data and fails to generalize; use regularization or more data."
    },
    {
        "id": 4,
        "q": "What is a confusion matrix?",
        "a": "A confusion matrix shows counts of true/false positives/negatives for a classifier, helping analyze performance."
    },
    {
        "id": 5,
        "q": "What is cross-validation?",
        "a": "Cross-validation splits data into folds to estimate generalization performance while tuning hyperparameters."
    }
]
