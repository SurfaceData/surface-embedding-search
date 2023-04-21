from pathlib import Path

from embedding_search.config import settings
from embedding_search.metadata_store.parquet_store import ParquetMetadataStore


def get_metadata_store():
    return ParquetMetadataStore(Path(f"{settings.DATA_PATH}/metadata"))


metadata_store = get_metadata_store()
