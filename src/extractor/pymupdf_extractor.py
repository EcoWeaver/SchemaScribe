from pathlib import Path

from errors import UserError


class PyMuPdfExtractor:
    # lazy import of the library the first time this class is called
    def __init__(self):
        try:
            import pymupdf  # type: ignore[import-not-found]
        except ImportError as e:
            raise UserError("Pymupdf is not installed or could not be found!") from e

        self._pymupdf = pymupdf

    def to_markdown(self, pdf_path: Path) -> str:
        doc = self._pymupdf.open(str(pdf_path))
        # rapidocr package is needed for ocr usage, maybe we can add it later
        return doc.to_markdown(use_ocr=False)  # type: ignore[attr-defined]
