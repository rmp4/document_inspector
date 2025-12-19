import logging
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

from docling.document_converter import DocumentConverter

from app.utils.bbox import DoclingBBox, normalize_bbox

logger = logging.getLogger(__name__)

_converter_lock = Lock()
_converter_instance: DocumentConverter | None = None


def get_converter() -> DocumentConverter:
    global _converter_instance
    if _converter_instance is None:
        with _converter_lock:
            if _converter_instance is None:
                logger.info("Initializing Docling DocumentConverter")
                _converter_instance = DocumentConverter()
    return _converter_instance


@dataclass(frozen=True)
class ParseResult:
    markdown: str
    bbox_map: list[dict]


def parse_pdf(path: str | Path) -> ParseResult:
    converter = get_converter()
    result = converter.convert(str(path))
    document = result.document
    markdown = document.export_to_markdown()
    doc_dict = document.export_to_dict()
    pages = getattr(document, "pages", {})

    bbox_map: list[dict] = []
    for item in doc_dict.get("texts", []):
        for prov in item.get("prov", []):
            bbox = prov.get("bbox")
            if not bbox:
                continue
            normalized = normalize_bbox(
                DoclingBBox(
                    left=bbox["l"],
                    top=bbox["t"],
                    right=bbox["r"],
                    bottom=bbox["b"],
                    page_no=prov.get("page_no", 1),
                ),
                page_height=_page_height_for_prov(pages, prov),
            )
            bbox_map.append({"text": item.get("text", ""), "bbox": normalized})

    return ParseResult(markdown=markdown, bbox_map=bbox_map)


def _page_height_for_prov(pages: dict, prov: dict) -> float:
    page_no = prov.get("page_no", 1)
    page = pages.get(page_no)
    if page is None:
        return 0.0
    return float(getattr(page.size, "height", 0.0))
