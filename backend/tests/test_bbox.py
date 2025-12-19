from app.utils.bbox import DoclingBBox, normalize_bbox


def test_normalize_bbox_flips_y_axis() -> None:
    bbox = DoclingBBox(left=10, top=100, right=60, bottom=140, page_no=1)
    result = normalize_bbox(bbox, page_height=200)
    assert result == [10, 60, 50, 40, 1.0]
