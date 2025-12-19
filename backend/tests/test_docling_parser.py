from pathlib import Path

from reportlab.pdfgen import canvas

from app.engine.parser import get_converter, parse_pdf


def _make_pdf(path: Path) -> None:
    pdf = canvas.Canvas(str(path))
    pdf.drawString(100, 700, "Hello Docling")
    pdf.save()


def test_parser_returns_markdown_and_bbox(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    _make_pdf(pdf_path)
    result = parse_pdf(pdf_path)
    assert "Hello Docling" in result.markdown
    assert result.bbox_map
    assert "bbox" in result.bbox_map[0]


def test_converter_singleton() -> None:
    first = get_converter()
    second = get_converter()
    assert first is second
