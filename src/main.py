import json
import sys
from pathlib import Path

from cli.arguments import parse_arguments
from errors import UserError
from extractor.extract import extract_pdfs
from llm_api_caller import manager
from llm_api_caller.errors_plugin_caller import UnknownPluginError


def run():
    args = parse_arguments()
    # print(args) # for debug purposes only

    # extract information from pdf via given library
    extracted_files = extract_pdfs(args.pdf, args.recursive, args.extractor)

    try:
        # manager = Plugin_manager()
        plugin_cls = manager.get(args.name_Plugin)
    except UnknownPluginError as e:
        sys.exit(str(e))
    api_caller = plugin_cls(
        args.base_url,
        args.api_key,
        args.model,
        args.temperature,
        args.timeout_llm,
        args.max_retries,
        args.max_tokens,
        args.top_p,
        args.provider,
    )  # TODO extra param

    # TODO
    #   - Promt
    #   - Extract given class frome the LinkLM schema and save as Json
    #   - fuse Promt, schema class and extrated text

    prompt_path = Path("prompt") / "prompt.txt"  # Temporary
    prompt = prompt_path.read_text(encoding="utf-8")  # Temporary
    prompt = f"{prompt}\n\nText:\n{extracted_files}"  # Temporary

    print("calling LLM...")  # Temporary
    result = api_caller.call_api(prompt)  # Temporary

    # TODO save json

    # print rep in the terminal Temporary
    print("\n--- ANSWER ---")
    print(json.dumps(result["answer"], indent=4, ensure_ascii=False))
    print("\n--- REASONING ---")
    print(result["reasoning"])
    print("\n--- TOKEN USAGE ---")
    print(f"Prompt tokens:     {result['prompt_tokens']}")
    print(f"Completion tokens: {result['completion_tokens']}")
    print(f"Total tokens:      {result['total_tokens']}")


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
