import jsonlines
import pandas as pd
import typer

from pathlib import Path

app = typer.Typer()


@app.command()
def smithsonian(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    jsonl_files = input_dir.glob("*.txt")
    for jsonl_file in jsonl_files:
        with jsonlines.open(jsonl_file) as reader:
            for obj in reader:
                # Do a lot of data validation to make sure no critical
                # fields are missing.  Also reject anything that isn't
                # explicitly CC0.
                if "content" not in obj:
                    continue
                content = obj["content"]
                if "descriptiveNonRepeating" not in content:
                    continue
                descriptiveNonRepeating = content["descriptiveNonRepeating"]
                if "online_media" not in descriptiveNonRepeating:
                    continue
                online_media = descriptiveNonRepeating["online_media"]
                if "media" not in online_media:
                    continue
                media = online_media["media"]
                if len(media) == 0:
                    continue
                primary_media = media[0]
                if "type" not in primary_media:
                    continue
                if primary_media["type"] != "Images":
                    continue
                if "usage" not in primary_media:
                    continue
                usage = primary_media["usage"]
                if "access" not in usage:
                    continue
                if usage["access"] != "CC0":
                    continue
                if "content" not in primary_media:
                    continue
                id = obj["id"]
                title = obj["title"]
                url = primary_media["content"]
                thumbnail_url = primary_media["thumbnail"]
                if not thumbnail_url:
                    thumbnail_url = ""
                rows.append([id, title, url, thumbnail_url])

    # Write all the data!
    df = pd.DataFrame(rows, columns=["id", "title", "url", "thumbnail_url"])
    df.to_csv(output_dir / "urls.tsv", sep="\t", index=False)
