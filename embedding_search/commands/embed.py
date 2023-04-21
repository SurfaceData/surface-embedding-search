import json
import numpy as np
import pandas as pd
import torch

from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from typing import List
from webdataset import handle_extension, WebDataset
from PIL import Image

from embedding_search.models.embedding_model import EmbeddingModel
from embedding_search.models.open_clip import OpenClipTextModel


class DownloadedDataset(WebDataset):
    def __init__(self, input_dir: Path, model: EmbeddingModel):
        WebDataset.__init__(self, [str(path) for path in input_dir.glob("*.tar")])

        def decoder(value):
            return model.prepare(value.decode("utf-8"))

        self.decode(handle_extension(".txt", decoder)).to_tuple("txt", "json")


class ShardedOutputWriter:
    def __init__(self, output_dir: Path, shard_limit: int = 64):
        self.shard_limit = shard_limit
        self.output_dir = output_dir

        self.current_shard = 0
        self.embeddings = []
        self.metadata = []
        self.shard_size = 0

    def __call__(self, new_embeddings, new_metadatas):
        new_size = len(new_embeddings)
        if (self.shard_size + new_size) > self.shard_limit:
            self.flush()

        self.embeddings.append(new_embeddings)
        self.metadata.extend(new_metadatas)  # [json.loads(m) for m in new_metadatas])
        self.shard_size += new_size

    def save_array(self, array, prefix):
        matrix = np.concatenate(array)
        if len(matrix) == 0:
            return

        result_dir = self.output_dir / prefix
        result_dir.mkdir(exist_ok=True)
        result_file = result_dir / f"{self.current_shard:03d}.npy"
        with open(result_file, "wb") as f:
            np.save(f, matrix)

    def flush(self):
        if len(self.embeddings) == 0:
            return
        self.save_array(self.embeddings, "text_emb")

        df = pd.json_normalize(self.metadata)
        metadata_dir = self.output_dir / "metadata"
        metadata_dir.mkdir(exist_ok=True)
        metadata_file = metadata_dir / f"{self.current_shard:03d}.parquet"
        with open(metadata_file, "wb") as f:
            df.to_parquet(f)

        self.current_shard += 1
        self.embeddings = []
        self.metadata = []
        self.shard_size = 0


def embed(
    input_dir: Path,
    output_dir: Path,
    device: str = "cuda",
    model_id: str = "coca_ViT-B-32",
    batch_size: int = 32,
    shard_limit: int = 100_000,
):
    output_dir.mkdir(parents=True, exist_ok=True)

    output_writer = ShardedOutputWriter(output_dir, shard_limit=shard_limit)

    model = OpenClipTextModel(model_id, False, device)

    data = DownloadedDataset(input_dir, model).batched(batch_size)
    loader = DataLoader(data, batch_size=None, shuffle=False)
    for step, (tokenized, metadatas) in tqdm(enumerate(loader)):
        embeddings = model.embed(tokenized)
        output_writer(embeddings, metadatas)
    output_writer.flush()
