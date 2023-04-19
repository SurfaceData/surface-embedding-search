import pandas as pd

from pathlib import Path

from embedding_search.metadata_store.metadata_store import MetadataStore


class ParquetMetadataStore(MetadataStore):
    def __init__(self, data_dir: Path):
        files = sorted(data_dir.glob("*.parquet"))
        self.df = pd.concat(
            pd.read_parquet(parquet_file, engine="pyarrow") for parquet_file in files
        )

    def get(self, ids, columns=None):
        return self.df.iloc[ids].to_dict(orient="records")
