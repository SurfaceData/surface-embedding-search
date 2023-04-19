from abc import ABC, abstractmethod


class MetadataStore(ABC):
    @abstractmethod
    def get(self, ids, columns=None):
        raise NotImplemented
