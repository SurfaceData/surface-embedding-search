from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Dict, List

from embedding_search.auth import validate_api_key
from embedding_search.metadata_store.factory import metadata_store

router = APIRouter(tags=["search"], dependencies=[Depends(validate_api_key)])


class SearchItem(BaseModel):
    fields: Dict[str, Any]


class SearchResult(BaseModel):
    items: List[SearchItem]
    total: int


@router.get("/search")
def search(query: str) -> SearchResult:
    items = []
    total = 0
    return SearchResult(items=items, total=total)
