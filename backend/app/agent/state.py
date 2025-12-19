from typing import TypedDict


class AuditState(TypedDict, total=False):
    input_text: str
    decision: str
    notes: str
