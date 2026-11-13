import argparse
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

    # llm model (accessed either locally or via api)
    modelGroup = parser.add_mutually_exclusive_group(required=True)
    modelGroup.add_argument("--local", help="...")
    modelGroup.add_argument("--api", help="...")

    # output format
    parser.add_argument("--outputFormat", required=False, default="rdf", help="...")

    args = parser.parse_args()

    # check if given input paths are valid
    validate_paths(args.pdf)
    validate_paths(args.schema)

    return args
