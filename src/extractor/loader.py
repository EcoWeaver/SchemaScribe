import importlib
from pathlib import Path
from typing import Protocol, runtime_checkable

from errors import UserError


@runtime_checkable
class PdfExtractor(Protocol):
    def to_markdown(self, pdf_path: Path) -> str: ...


SUPPORTED_EXTRACTORS = {
    "docling": "extractor.docling_extractor:DoclingExtractor",
    "marker": "extractor.marker_extractor:MarkerExtractor",
    "pymupdf": "extractor.pymupdf_extractor:PyMuPdfExtractor",
    # "alias": "extractor.alias:className",
}


def load_extractor(extractor_name) -> PdfExtractor:
    extr = SUPPORTED_EXTRACTORS.get(extractor_name, extractor_name)
    if ":" not in extr:
        available_extractors = " | ".join(SUPPORTED_EXTRACTORS)
        raise UserError(
            f"The given extractor <{extractor_name}> is not supported! "
            f"Available extractors: {available_extractors}"
        )

    module_name, class_name = extr.split(":", 1)

    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        raise UserError(
            f"Extractor <{extractor_name}> could not be loaded correctly! "
            f"Please make sure the respective library is installed: {e}"
        ) from e

    try:
        extractor = getattr(module, class_name)()
    except AttributeError as e:
        raise RuntimeError(
            f"Class <{class_name}> not found in module <{module_name}>"
        ) from e

    # check if extractor correctly implements our base class
    if not isinstance(extractor, PdfExtractor):
        raise TypeError(
            f"The extractor <{extractor_name}> is not correctly implemented!"
        )

    return extractor
