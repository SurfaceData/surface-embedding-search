from tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY ./requirements.txt /app/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip pip \
  install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./main.py /app/main.py
COPY ./embedding_search /app/embedding_search

ENV PORT 8080
EXPOSE 8080
