# Surface Embedding Search

This is a [FastAPI](https://fastapi.tiangolo.com/) based rewrite of [Clip
Retrieval](https://github.com/rom1504/clip-retrieval).

It includes a [Typer](https://typer.tiangolo.com/) command line tool for
preparing datasets for serving and a simple Dockerfile to make an image and
get it running.

This is still a work in progress and is unstable but should generally work
with a bit of effort.

TODOs:
*  Generalize data preparation to be more flexible
*  Support multiple indices for the same dataset

## Getting Started

The major dependencies are:
*  Python 3.10
*  pip
*  Docker 

Get that all setup and create a conda environment (or virtualenv) with something like:

```sh
conda create -n surface-embedding-search python=3.10
```

## Preparing a dataset

This is a multi-step process.  One day it'll be easier:

First, set your base dataset directory to a env variable such as `DATA_DIR`.

Then:

```sh
python -m cli prepare smithsonian ${DATA_DIR}/raw ${DATA_DIR}/prepared
python -m cli download ${DATA_DIR}/prepared ${DATA_DIR}/dataset
python -m cli embed ${DATA_DIR}/dataset ${DATA_DIR}/embed
python -m cli index ${DATA_DIR}/dataset ${DATA_DIR}/index
```

That prepares the full index ready for serving.  To serve, you can run locally with:

```sh
uvicorn main:app
```

After you've set some env variables in a `.env` file.

To serve with Docker, build the image with:

```sh
DOCKER_BUILDKIT=1 docker build -t your-org/embedding-search .
```

If you like using Docker Compose for running things, this compose script works well:

```yaml
version: '3.5'

services:
  embedding-search:
    container_name: embedding-search
    image: your-org/embedding-search
    restart: always
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              device_ids: ['1']
              capabilities: [gpu]
    networks:
      - hosting
    expose: 
      - "8080"
    volumes:
      - ${DATA_DIR}/index:/index
    environment:
      - MAX_WORKERS=1
      - TIMEOUT=360
      - DATA_PATH=/index
      - DEVICE=cuda
      - MODEL_ID=coca_ViT-B-32
      - LETSENCRYPT_HOST=your-host.hostname.com
      - VIRTUAL_HOST=your-host.hostname.com
      - VIRTUAL_PORT=8080

networks:
  hosting:
    name: hosting
    external: true
```

This leverages a
[nginxproxy/nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) with a
[nginxproxy/acme-companion](https://github.com/nginx-proxy/acme-companion)
to guard everything with a pre-configured NGinx setup and SSL certificates
provided by certbot.
