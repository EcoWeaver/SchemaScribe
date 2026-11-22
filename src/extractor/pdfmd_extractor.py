import tempfile
from pathlib import Path

from errors import UserError


class PdfmdExtractor:
    # lazy import of the library the first time this class is called
    def __init__(self):
        try:
            from pdfmd import Options, pdf_to_markdown  # type: ignore[import-not-found]
        except ImportError as e:
            raise UserError("pdfmd is not installed or could not be found!") from e

        self._options_cls = Options
        self._pdf_to_markdown = pdf_to_markdown

    def to_markdown(self, pdf_path: Path) -> str:
        # pdfmd writes its result to a file, so we use a temp dir and read it back
        # (it may also export images next to the .md, which we simply discard)
        with tempfile.TemporaryDirectory() as tmp:
            out_md = Path(tmp) / f"{pdf_path.stem}.md"
            self._pdf_to_markdown(
                str(pdf_path), str(out_md), options=self._options_cls()
            )

            # pdfmd avoids overwrites by adding suffixes, so fall back to a search
            if not out_md.exists():
                candidates = sorted(Path(tmp).glob("*.md"))
                if not candidates:
                    raise RuntimeError("pdfmd did not produce any Markdown file")
                out_md = candidates[0]

            return out_md.read_text(encoding="utf-8")

    def to_json(self, pdf_path: Path) -> str:
        # pdfmd only produces Markdown
        raise NotImplementedError("pdfmd does not support JSON output")