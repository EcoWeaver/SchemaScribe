import os
import shutil
from pathlib import Path

from errors import UserError

# Marker 2.x conversion modes: no_ocr | fast | balanced | vllm
# (aliases: indra = fast, surya / accurate = vllm).
# "vllm" runs full-page Surya VLM OCR on every page; override via MARKER_MODE.
DEFAULT_MODE = "vllm"
VLM_ONLY_MODES = ("vllm", "surya", "accurate")  # skip pdftext and Indra entirely
NO_SERVER_MODES = ("no_ocr", "fast", "indra")  # fully in-process, no VLM server


class MarkerExtractor:
    def __init__(self):
        self._mode = os.environ.get("MARKER_MODE", DEFAULT_MODE)
        self._models = None
        self._converters = {}

    def _check_server_backend(self):
        # modes using the Surya VLM need an inference server, which Marker spawns:
        # vLLM via Docker (NVIDIA GPU) or llama.cpp (CPU / Apple Silicon)
        if self._mode in NO_SERVER_MODES or os.environ.get("SURYA_INFERENCE_URL"):
            return
        if shutil.which("llama-server") is None and shutil.which("docker") is None:
            raise UserError(
                f"Marker mode <{self._mode}> needs an inference backend: "
                "install llama.cpp (macOS: `brew install llama.cpp`) or Docker "
                "with the NVIDIA Container Toolkit, or set SURYA_INFERENCE_URL."
            )

    # create converter (and load models) only the first time this is called;
    # one converter per output format, all sharing the same models/server
    def _get_converter(self, output_format="markdown"):
        if output_format not in self._converters:
            try:
                from marker.config.parser import ConfigParser  # type: ignore[import-not-found]
                from marker.converters.pdf import PdfConverter  # type: ignore[import-not-found]
                from marker.models import create_model_dict  # type: ignore[import-not-found]
            except ImportError as e:
                raise UserError("Marker is not installed or could not be found!") from e

            if self._models is None:
                self._check_server_backend()
                # mirrors what marker's own CLI (marker_single) does per mode
                self._models = create_model_dict(
                    load_indra=self._mode not in VLM_ONLY_MODES,
                    no_server=self._mode in NO_SERVER_MODES,
                )

            # ConfigParser to pick renderer ("output_format" in config not enough)
            parser = ConfigParser({"mode": self._mode, "output_format": output_format})
            self._converters[output_format] = PdfConverter(
                config=parser.generate_config_dict(),
                artifact_dict=self._models,
                processor_list=parser.get_processors(),
                renderer=parser.get_renderer(),
                llm_service=parser.get_llm_service(),
            )

        return self._converters[output_format]

    def _convert(self, pdf_path: Path, output_format: str) -> str:
        converter = self._get_converter(output_format)
        from marker.output import text_from_rendered  # type: ignore[import-not-found]

        # returns (text, file extension, images) ---> we only take the first one
        text, _, _ = text_from_rendered(converter(str(pdf_path)))

        return text

    def to_markdown(self, pdf_path: Path) -> str:
        return self._convert(pdf_path, "markdown")

    def to_json(self, pdf_path: Path) -> str:
        return self._convert(pdf_path, "json")