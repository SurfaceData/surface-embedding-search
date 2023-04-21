from abc import ABC, abstractmethod

from typing import Any, List


class EmbeddingModel(ABC):
    @abstractmethod
    def prepare(self, value: Any):
        pass

    @abstractmethod
    def embed(self, value: List[Any]):
        pass
