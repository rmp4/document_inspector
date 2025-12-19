from uuid import uuid4

from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.agent.checkpoint import get_checkpointer
from app.agent.graph import build_graph

router = APIRouter()


class AuditStartRequest(BaseModel):
    input_text: str = Field(default="trace demo")


class AuditStartResponse(BaseModel):
    thread_id: str
    interrupt: list | dict | None


class AuditResumeRequest(BaseModel):
    thread_id: str
    decision: str
    notes: str | None = None


class AuditResumeResponse(BaseModel):
    thread_id: str
    decision: str
    notes: str


@router.post("/audit/start", response_model=AuditStartResponse)
async def start_audit(payload: AuditStartRequest) -> AuditStartResponse:
    checkpointer = get_checkpointer()
    if checkpointer is None:
        raise HTTPException(status_code=503, detail="Checkpointer not initialized.")

    thread_id = str(uuid4())
    graph = build_graph(checkpointer=checkpointer)
    result = await graph.ainvoke(
        {"input_text": payload.input_text},
        config={"configurable": {"thread_id": thread_id}},
    )
    return AuditStartResponse(thread_id=thread_id, interrupt=result.get("__interrupt__"))


@router.post("/audit/resume", response_model=AuditResumeResponse)
async def resume_audit(payload: AuditResumeRequest) -> AuditResumeResponse:
    checkpointer = get_checkpointer()
    if checkpointer is None:
        raise HTTPException(status_code=503, detail="Checkpointer not initialized.")

    graph = build_graph(checkpointer=checkpointer)
    command = Command(resume={"decision": payload.decision, "notes": payload.notes or ""})
    result = await graph.ainvoke(
        command,
        config={"configurable": {"thread_id": payload.thread_id}},
    )
    return AuditResumeResponse(
        thread_id=payload.thread_id,
        decision=str(result.get("decision", payload.decision)),
        notes=str(result.get("notes", payload.notes or "")),
    )
