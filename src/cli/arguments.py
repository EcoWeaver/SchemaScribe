import argparse
import json
from pathlib import Path

from errors import UserError


def validate_paths(path_list):
    # collect all non existing paths
    missing_paths = [path for path in path_list if not path.exists()]

    if missing_paths:
        raise UserError(
            "The following paths could not be found:\n"
            + "\n".join(str(path) for path in missing_paths)
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="SchemaScribe",
        description="...",
        usage="%(prog)s [options]",
    )

    # input pdf files (as single / multiple files or whole dir ---> resolved later)
    parser.add_argument("--pdf", nargs="+", type=Path, required=True, help="...")

    # input pdf files (as single / multiple files or whole dir ---> resolved later)
    parser.add_argument("--recursive", "-r", action="store_true", help="...")

    # input linkML / CAMO schema
    parser.add_argument("--schema", nargs="+", type=Path, required=True, help="...")
    # TODO: do we allow more than 1 input schema?

    # name of pdf extraction library
    parser.add_argument(
        "--extractor",
        choices=["pymupdf", "docling", "marker"],
        required=False,
        default="pymupdf",
        help="...",
    )

    # llm model informations (accesse via api)
    parser.add_argument("--name_Plugin", default="litellm", type=str)
    parser.add_argument(
        "--base_url",
        required=True,
        help="Base URL is the API URL used to call your LLM model.",
    )
    parser.add_argument("--api_key", required=True, help="Your access key")
    parser.add_argument("--model", required=True)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--top_p", type=float, default=None)
    parser.add_argument("--timeout_llm", type=int, default=1200, help="in seconds")
    parser.add_argument("--max_retries", type=int, default=2)
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "gemini"],
        default="openai",
        help="API format",
    )
    parser.add_argument(
        "--extra_params",
        type=json_dict,
        default={},
    )
    # TODO extra Parameter

    # output format
    parser.add_argument("--outputFormat", required=False, default="rdf", help="...")

    args = parser.parse_args()

    # check if given input paths are valid
    validate_paths(args.pdf)
    validate_paths(args.schema)

    return args


def json_dict(text: str) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as e:
        raise argparse.ArgumentTypeError(f"invalid JSON: {e}")
    if not isinstance(value, dict):
        raise argparse.ArgumentTypeError("must be a JSON object, e.g. '{\"key\": 1}'")
    return value
