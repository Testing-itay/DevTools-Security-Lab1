"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Agent(BaseModel):
    """Agent model for orchestration."""

    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=200)
    model: str = Field(default="gpt-4", max_length=50)
    created_at: Optional[datetime] = None


class AnalysisRequest(BaseModel):
    """Request payload for code analysis."""

    code: str = Field(..., min_length=1)
    language: str = Field(default="python", max_length=20)
    include_suggestions: bool = True


class AnalysisResult(BaseModel):
    """Result of code analysis."""

    request_id: str
    findings: list[dict] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response with system status."""

    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    cache: str = "connected"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
