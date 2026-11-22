import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from errors import UserError

#! Currently dropped due to compatibility issues

# appjsonify needs a layout template matching the paper's publisher style
# (AAAI, ACL, ICML, ICLR, NeurIPS, IEEE, ACM, Springer; a trailing "2" selects
# the faster, rule-based and noisier variant, e.g. "ACL2").
# Can be overridden via the environment variable APPJSONIFY_PAPER_TYPE.
DEFAULT_PAPER_TYPE = "ACL2"


class AppJsonifyExtractor:
    # appjsonify documents only a CLI, so we call that instead of a Python API.
    def __init__(self, paper_type=None):
        self._paper_type = paper_type or os.environ.get(
            "APPJSONIFY_PAPER_TYPE", DEFAULT_PAPER_TYPE
        )

        # look on PATH first, then next to the running interpreter (venv case)
        cli = shutil.which("appjsonify")
        if cli is None:
            candidate = Path(sys.executable).parent / "appjsonify"
            cli = str(candidate) if candidate.exists() else None
        if cli is None:
            raise UserError("appjsonify is not installed or could not be found!")

        self._cli = cli

    def to_markdown(self, pdf_path: Path) -> str:
        # appjsonify only produces JSON; the test runner treats this as "unsupported"
        raise NotImplementedError("appjsonify only supports JSON output")

    def to_json(self, pdf_path: Path) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            cmd = [
                self._cli,
                str(pdf_path),
                str(out_dir),
                "--paper_type",
                self._paper_type,
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                raise RuntimeError(
                    f"appjsonify exited with code {proc.returncode}: "
                    f"{proc.stderr.strip()[-500:]}"
                )

            # expected output is <pdf stem>.json, but we do not rely on it
            json_files = sorted(out_dir.rglob("*.json"))
            if not json_files:
                raise RuntimeError("appjsonify did not produce JSON file")
            preferred = [f for f in json_files if f.stem == pdf_path.stem]
            result_file = (preferred or json_files)[0]

            data = json.loads(result_file.read_text(encoding="utf-8"))
            return json.dumps(data, ensure_ascii=False, indent=2)