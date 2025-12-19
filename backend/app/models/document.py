from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
    docling_markdown: str
    docling_bbox_map: list[dict[str, Any]] = Field(
        sa_column=Column(JSONB, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
