from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel

from core.database import get_db

router = APIRouter()


class AgentCreate(BaseModel):
    name: str
    role: str
    prompt: str
    knowledge_domains: List[str] = []
    config: dict = {}


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    prompt: str
    knowledge_domains: List[str]
    config: dict


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return []


@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate, db: AsyncSession = Depends(get_db)):
    return {
        "id": "temp-id",
        "name": agent.name,
        "role": agent.role,
        "prompt": agent.prompt,
        "knowledge_domains": agent.knowledge_domains,
        "config": agent.config,
    }


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=404, detail="Agent not found")


@router.post("/{agent_id}/execute")
async def execute_agent(agent_id: str, task: str, db: AsyncSession = Depends(get_db)):
    return {
        "agent_id": agent_id,
        "task": task,
        "status": "completed",
        "result": "Task completed successfully",
    }
