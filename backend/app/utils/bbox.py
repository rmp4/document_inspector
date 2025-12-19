from dataclasses import dataclass


@dataclass(frozen=True)
class DoclingBBox:
    left: float
    top: float
    right: float
    bottom: float
    page_no: int


def normalize_bbox(bbox: DoclingBBox, page_height: float) -> list[float]:
    x = bbox.left
    y = page_height - bbox.top
    w = bbox.right - bbox.left
    h = bbox.bottom - bbox.top
    return [x, y, w, h, float(bbox.page_no)]
