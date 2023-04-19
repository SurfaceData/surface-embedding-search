from pathlib import Path

from embedding_search.metadata_store.parquet_store import ParquetMetadataStore


def get_metadata_store():
    return ParquetMetadataStore(Path("data"))


metadata_store = get_metadata_store()
