from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from core.database import get_db

router = APIRouter()


class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    definition: dict


@router.get("/")
async def list_workflows(db: AsyncSession = Depends(get_db)):
    return []


@router.post("/", status_code=201)
async def create_workflow(workflow: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    return {
        "id": "temp-workflow-id",
        "name": workflow.name,
        "description": workflow.description,
        "definition": workflow.definition,
    }
