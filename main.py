from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics
from typing import List, Union

from embedding_search.routes import search

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="surface-embedding-search")
app.add_route("/metrics", handle_metrics)

app.include_router(search.router)


@app.get("/health")
def health():
    """Handles basic health checks."""
    return {}
