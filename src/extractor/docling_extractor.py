from pathlib import Path

from errors import UserError


class DoclingExtractor:
    def __init__(self):
        self._converter = None

    # create converter object only the first time this is called
    def _get_converter(self):
        if self._converter is None:
            try:
                from docling.document_converter import DocumentConverter
            except ImportError as e:
                raise UserError(
                    "Docling is not installed or could not be found!"
                ) from e
            self._converter = DocumentConverter()

        return self._converter

    def to_markdown(self, pdf_path: Path) -> str:
        result = self._get_converter().convert(str(pdf_path))
        return result.document.export_to_markdown()
