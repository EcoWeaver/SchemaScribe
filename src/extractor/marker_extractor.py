from pathlib import Path

from errors import UserError


class MarkerExtractor:
    def __init__(self):
        self._converter = None
        # self._text_from_rendered = None

    # create converter (and load models) only the first time this is called
    def _get_converter(self):
        if self._converter is None:
            try:
                from marker.converters.pdf import PdfConverter
                from marker.models import create_model_dict
                # from marker.output import text_from_rendered
            except ImportError as e:
                raise UserError("Marker is not installed or could not be found!") from e
            self._converter = PdfConverter(
                artifact_dict=create_model_dict(),
                config={"disable_ocr": True},
            )
            # self._text_from_rendered = text_from_rendered

        return self._converter

    def to_markdown(self, pdf_path: Path) -> str:
        converter = self._get_converter()
        from marker.output import text_from_rendered

        # returns (markdown_text, metadata, images) ---> we only take the first one
        text, _, _ = text_from_rendered(converter(str(pdf_path)))

        return text
