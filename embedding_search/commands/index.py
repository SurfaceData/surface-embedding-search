from autofaiss import build_index
from distutils.dir_util import copy_tree
from pathlib import Path


def index(
    input_dir: Path,
    output_dir: Path,
    max_memory: str = "4G",
    current_memory: str = "16G",
):
    output_dir.mkdir(parents=True, exist_ok=True)

    embed_dir = input_dir / "text_emb"
    if embed_dir.exists():
        build_index(
            embeddings=str(embed_dir),
            index_path=str(output_dir / "text.index"),
            index_infos_path=str(output_dir / "text.json"),
            max_index_memory_usage=max_memory,
            current_memory_available=current_memory,
        )
    copy_tree(str(input_dir / "metadata"), str(output_dir / "metadata"))
