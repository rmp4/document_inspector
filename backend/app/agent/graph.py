from langgraph.graph import END, StateGraph
from langgraph.types import interrupt

from app.agent.state import AuditState


def _audit(state: AuditState) -> AuditState:
    return {"decision": "needs_review", "notes": "pending human review"}


def _human_review(state: AuditState) -> AuditState:
    resume_value = interrupt({"state": state, "action": "human_review"})
    if isinstance(resume_value, dict):
        decision = str(resume_value.get("decision", "approved"))
        notes = str(resume_value.get("notes", ""))
    else:
        decision = str(resume_value)
        notes = ""
    return {"decision": decision, "notes": notes}


def build_graph(checkpointer=None):
    graph = StateGraph(AuditState)
    graph.add_node("audit", _audit)
    graph.add_node("human_review", _human_review)
    graph.add_edge("audit", "human_review")
    graph.add_edge("human_review", END)
    graph.set_entry_point("audit")
    return graph.compile(checkpointer=checkpointer)
