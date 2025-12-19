from dataclasses import dataclass


@dataclass(frozen=True)
class DoclingBBox:
    left: float
    top: float
    right: float
    bottom: float
    page_no: int


def normalize_bbox(bbox: DoclingBBox, page_height: float) -> list[float]:
    x = min(bbox.left, bbox.right)
    w = abs(bbox.right - bbox.left)
    top_edge = max(bbox.top, bbox.bottom)
    bottom_edge = min(bbox.top, bbox.bottom)
    y = page_height - top_edge
    h = top_edge - bottom_edge
    return [x, y, w, h, float(bbox.page_no)]
