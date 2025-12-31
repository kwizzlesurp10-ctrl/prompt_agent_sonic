from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()


@router.get("/search")
async def search_knowledge(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
):
    return {"query": q, "count": 0, "results": []}


@router.get("/stats")
async def get_stats():
    return {"total_tools": 0, "categories": 0, "status": "initializing"}


@router.get("/categories")
async def list_categories():
    return []
