import sys

from cli.arguments import parse_arguments
from errors import UserError
from extractor.extract import extract_pdfs


def run():
    args = parse_arguments()
    # print(args) # for debug purposes only

    # extract information from pdf via given library
    extract_pdfs(args.pdf, args.recursive, args.extractor)

    # ...


def main():
    # catch and handle all user induced errors
    try:
        run()
    except UserError as e:
        print(f"\nERROR >>> {e}", file=sys.stderr)
        print("  ---->   exiting ...", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
