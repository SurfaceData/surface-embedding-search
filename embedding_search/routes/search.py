import faiss
import torch

from fastapi import APIRouter, Depends
from loguru import logger
from pydantic import BaseModel
from typing import Any, Dict, List

from embedding_search.auth import validate_api_key
from embedding_search.config import settings
from embedding_search.metadata_store.factory import metadata_store
from embedding_search.models.factory import get_model

router = APIRouter(tags=["search"], dependencies=[Depends(validate_api_key)])

logger.info("loading model")
model = get_model()
logger.info("loading index")
index = faiss.read_index(f"{settings.DATA_PATH}/text.index")


class SearchItem(BaseModel):
    fields: Dict[str, Any]


class SearchResult(BaseModel):
    items: List[SearchItem]
    total: int


@router.get("/search")
def search(query: str, numResults: int = 32) -> SearchResult:
    prepared_text = model.prepare(query)
    embedding = model.embed(prepared_text)
    _, indices, _ = index.search_and_reconstruct(embedding, 32)

    items = []
    total = 0
    return SearchResult(items=items, total=total)
