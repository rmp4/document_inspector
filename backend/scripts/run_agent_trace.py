import os

from app.agent.checkpoint import close_checkpointer, init_checkpointer
from app.agent.graph import build_graph
from app.agent.monitoring import get_langfuse_client


async def main() -> None:
    os.environ.setdefault(
        "DATABASE_URL", "postgresql://docling:docling@localhost:5432/docling"
    )
    checkpointer = await init_checkpointer()
    graph = build_graph(checkpointer=checkpointer)

    await graph.ainvoke(
        {"input_text": "trace demo"},
        config={"configurable": {"thread_id": "trace-demo"}},
    )

    langfuse = get_langfuse_client()
    if langfuse is None:
        print("Langfuse client not configured; skip trace export.")
        await close_checkpointer()
        return

    trace_id = langfuse.create_trace_id()
    with langfuse.start_as_current_span(
        trace_context={"trace_id": trace_id},
        name="agent.run",
        input={"input_text": "trace demo"},
        metadata={"component": "langgraph"},
    ) as span:
        langfuse.update_current_trace(
            name="agent-trace",
            tags=["env:dev", "model:gemini-2"],
        )
        with langfuse.start_as_current_observation(
            trace_context={"trace_id": trace_id, "parent_span_id": span.id},
            as_type="generation",
            name="mock-llm",
            model="gemini-2",
            input="trace demo",
            output="needs_review",
            usage_details={"input_tokens": 8, "output_tokens": 12, "total_tokens": 20},
        ):
            pass

    langfuse.flush()
    trace_url = langfuse.get_trace_url(trace_id=trace_id)
    print(f"trace_url={trace_url}")
    await close_checkpointer()


if __name__ == "__main__":
    import asyncio
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
