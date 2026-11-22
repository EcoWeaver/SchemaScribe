from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from errors import UserError
from extractor.loader import SUPPORTED_EXTRACTORS, load_extractor

# output format = extractor method name
FORMATS = {"md": "to_markdown", "json": "to_json"}
RESULTS_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class FormatResult:
    status: str  # "ok", "unsupported", "failed"
    seconds: float = 0.0
    chars: int = 0
    file: str | None = None
    error: str | None = None


def run_extraction_test(pdf_path, libraries):
    # Layout: <output_dir>/ext_res_<pdf stem>/<library>.md, <library>.json, summary.json
    pdf_path = Path(pdf_path).resolve()
    if pdf_path.suffix.lower() != ".pdf" or not pdf_path.is_file():
        raise UserError(f"<{pdf_path}> is not an existing PDF file.")

    target_dir = RESULTS_DIR / f"ext_res_{pdf_path.stem}"
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nExtraction test for <{pdf_path.name}> with {len(libraries)} library(ies)")
    print(f"Results will be saved to <{target_dir.resolve()}>")

    summary = {}
    for library in libraries:
        print(f"\n[{library}]")
        summary[library] = _test_library(library, pdf_path, target_dir)

    summary_file = target_dir / "summary.json"
    summary_file.write_text(
        json.dumps(
            {
                "pdf": str(pdf_path),
                "results": {
                    lib: {fmt: asdict(res) for fmt, res in results.items()}
                    for lib, results in summary.items()
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    _print_summary(summary)
    print(f"\nSummary saved to <{summary_file}>")
    return summary


def _test_library(library, pdf_path, target_dir):
    try:
        extractor = load_extractor(library)
    except Exception as e:
        print(f"  - Warning: could not load <{library}>: {e}")
        return {fmt: FormatResult("failed", error=f"load error: {e}") for fmt in FORMATS}

    # NOTE: the first call per library also includes lazy model loading,
    # so its timing is not directly comparable with the second one.
    return {
        fmt: _run_format(extractor, library, fmt, method_name, pdf_path, target_dir)
        for fmt, method_name in FORMATS.items()
    }


def _run_format(extractor, library, fmt, method_name, pdf_path, target_dir):
    method = getattr(extractor, method_name, None)
    if method is None:
        print(f"  - {fmt}: not supported (no <{method_name}>)")
        return FormatResult("unsupported")

    start = time.perf_counter()
    try:
        content = method(pdf_path)
    except NotImplementedError as e:
        print(f"  - {fmt}: not supported by this library")
        return FormatResult("unsupported", error=str(e) or None)
    except Exception as e:
        seconds = time.perf_counter() - start
        print(f"  - {fmt}: FAILED ({type(e).__name__}: {e})")
        return FormatResult(
            "failed", seconds=seconds, error=f"{type(e).__name__}: {e}"
        )
    seconds = time.perf_counter() - start

    if not isinstance(content, str):
        content = json.dumps(content, indent=2, ensure_ascii=False, default=str)

    safe_name = re.sub(r"[^A-Za-z0-9_-]+", "_", library)
    out_file = target_dir / f"{safe_name}.{fmt}"
    out_file.write_text(content, encoding="utf-8")

    print(f"  - {fmt}: ok ({len(content)} chars, {seconds:.1f}s) -> {out_file.name}")
    return FormatResult(
        "ok", seconds=seconds, chars=len(content), file=out_file.name
    )


def _print_summary(summary):
    width = max([len("library"), *(len(lib) for lib in summary)]) + 2
    line = "=" * (width + 44)
    print("\n" + line)
    print(f"{'library':<{width}}{'md':<22}{'json':<22}")
    print("-" * (width + 44))
    for library, results in summary.items():
        cells = []
        for fmt in FORMATS:
            res = results[fmt]
            if res.status == "ok":
                cells.append(f"ok {res.chars}c {res.seconds:.1f}s")
            else:
                cells.append(res.status)
        print(f"{library:<{width}}{cells[0]:<22}{cells[1]:<22}")
    print(line)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run all PDF extraction libraries on one PDF (MD + JSON)."
    )
    parser.add_argument("pdf", type=Path, help="the PDF to run all libraries on")
    parser.add_argument(
        "-l",
        "--libraries",
        nargs="+",
        default=list(SUPPORTED_EXTRACTORS),
        metavar="LIB",
        help="libraries to test (default: all registered in loader.py)",
    )
    args = parser.parse_args(argv)

    try:
        summary = run_extraction_test(args.pdf, args.libraries)
    except UserError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    failed = any(
        res.status == "failed" for results in summary.values() for res in results.values()
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())