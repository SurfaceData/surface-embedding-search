from img2dataset import download as img_download
from pathlib import Path


def download(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    img_download(
        url_list=str(input_dir),
        output_folder=str(output_dir),
        input_format="tsv",
        url_col="url",
        caption_col="title",
        extract_exif=False,
        save_additional_columns=["id", "thumbnail_url"],
        thread_count=16,
        output_format="webdataset",
        incremental_mode="incremental",
        retries=4,
    )
