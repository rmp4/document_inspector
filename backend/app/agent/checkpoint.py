import os
from typing import Optional

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

_checkpointer: Optional[AsyncPostgresSaver] = None
_checkpointer_cm = None


def _get_database_url() -> str:
    return os.environ.get(
        "DATABASE_URL", "postgresql://docling:docling@localhost:5432/docling"
    )


async def init_checkpointer() -> AsyncPostgresSaver:
    global _checkpointer, _checkpointer_cm
    if _checkpointer is not None:
        return _checkpointer

    conn_string = _get_database_url()
    _checkpointer_cm = AsyncPostgresSaver.from_conn_string(conn_string)
    _checkpointer = await _checkpointer_cm.__aenter__()
    await _checkpointer.setup()
    return _checkpointer


def get_checkpointer() -> Optional[AsyncPostgresSaver]:
    return _checkpointer


async def close_checkpointer() -> None:
    global _checkpointer, _checkpointer_cm
    if _checkpointer_cm is None:
        return
    await _checkpointer_cm.__aexit__(None, None, None)
    _checkpointer = None
    _checkpointer_cm = None
