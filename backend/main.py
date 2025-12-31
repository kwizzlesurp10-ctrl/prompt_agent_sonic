from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import agents, workflows, knowledge, auth
from core.database import init_db
from core.config import settings
from core.websocket import ConnectionManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting AgentCraft-Pro...")
    await init_db()
    print("✅ Database initialized")
    yield
    print("👋 Shutting down...")

app = FastAPI(
    title="AgentCraft-Pro API",
    description="Knowledge-augmented AI agent orchestration platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])

ws_manager = ConnectionManager()

@app.get("/")
async def root():
    return {
        "message": "Welcome to AgentCraft-Pro API",
        "version": "1.0.0",
        "docs":  "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "redis": "connected",
            "vectordb": "connected"
        }
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast(data, exclude=[client_id])
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
