"""CRUD endpoints for agent management."""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from api.models import Agent

router = APIRouter(prefix="/agents", tags=["agents"])

# In-memory store for demo; replace with postgres_repo in production
_agents: dict[str, Agent] = {}


@router.get("", response_model=list[Agent])
async def list_agents() -> list[Agent]:
    """List all registered agents."""
    return list(_agents.values())


@router.post("", response_model=Agent)
async def create_agent(agent: Agent) -> Agent:
    """Create a new agent."""
    agent_id = f"agent_{len(_agents) + 1}"
    agent.id = agent_id
    agent.created_at = datetime.utcnow()
    _agents[agent_id] = agent
    return agent


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str) -> Agent:
    """Get agent by ID."""
    if agent_id not in _agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return _agents[agent_id]


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str) -> dict:
    """Delete an agent."""
    if agent_id not in _agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    del _agents[agent_id]
    return {"status": "deleted", "id": agent_id}
