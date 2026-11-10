"""Agent execution API contract and non-blocking demonstration endpoint."""

import asyncio
import time
import uuid

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/agent", tags=["Agents"])


class AgentExecutionRequest(BaseModel):
    """Validated request for the simulated execution endpoint."""

    tenant_id: int = Field(gt=0)
    agent_id: int = Field(gt=0)
    prompt: str = Field(min_length=1, max_length=10_000)


class AgentExecutionResponse(BaseModel):
    """Structured simulated execution result."""

    execution_id: str
    tenant_id: int
    agent_id: int
    status: str
    output: str
    execution_time_seconds: float


@router.post("/execute", response_model=AgentExecutionResponse)
async def execute_agent(payload: AgentExecutionRequest) -> AgentExecutionResponse:
    """Simulate non-blocking work; no LLM is called by this endpoint."""
    started = time.perf_counter()
    await asyncio.sleep(0.4)
    return AgentExecutionResponse(
        execution_id=str(uuid.uuid4()),
        tenant_id=payload.tenant_id,
        agent_id=payload.agent_id,
        status="completed",
        output=f"Simulation completed for {len(payload.prompt)} prompt characters.",
        execution_time_seconds=round(time.perf_counter() - started, 6),
    )
