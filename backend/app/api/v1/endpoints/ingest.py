import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from app.core.database import get_session
from app.engine.parser import parse_pdf
from app.models.document import Document

router = APIRouter()


@router.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)) -> dict[str, str]:
    if not _is_pdf(file):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    tmp_path = _save_temp_pdf(file)
    try:
        result = parse_pdf(tmp_path)
        document = Document(
            filename=file.filename or "document.pdf",
            docling_markdown=result.markdown,
            docling_bbox_map=result.bbox_map,
        )
        with get_session() as session:
            session.add(document)
            session.commit()
            session.refresh(document)
        return {"doc_id": str(document.id)}
    finally:
        tmp_path.unlink(missing_ok=True)


def _is_pdf(file: UploadFile) -> bool:
    if file.content_type == "application/pdf":
        return True
    if file.filename and file.filename.lower().endswith(".pdf"):
        return True
    return False


def _save_temp_pdf(file: UploadFile) -> Path:
    suffix = Path(file.filename or "upload.pdf").suffix or ".pdf"
    handle, path = tempfile.mkstemp(suffix=suffix)
    os.close(handle)
    tmp_path = Path(path)
    with tmp_path.open("wb") as target:
        data = file.file.read()
        target.write(data)
    file.file.seek(0)
    return tmp_path
