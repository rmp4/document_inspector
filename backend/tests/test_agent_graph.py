import os

import pytest

from app.agent.checkpoint import close_checkpointer, init_checkpointer
from app.agent.graph import build_graph


@pytest.mark.anyio
async def test_graph_writes_checkpoint() -> None:
    os.environ.setdefault(
        "DATABASE_URL", "postgresql://docling:docling@localhost:5432/docling"
    )
    checkpointer = await init_checkpointer()
    graph = build_graph(checkpointer=checkpointer)

    result = await graph.ainvoke(
        {"input_text": "audit this"},
        config={"configurable": {"thread_id": "test-thread"}},
    )

    assert "__interrupt__" in result
    await close_checkpointer()
