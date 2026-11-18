import json
import sys
from pathlib import Path

from cli.arguments import parse_arguments
from errors import UserError
from extractor.extract import extract_pdfs
from llm_api_caller.liteLLM.litellm_API_caller import litellm_API_caller


def run():
    args = parse_arguments()
    # print(args) # for debug purposes only

    # extract information from pdf via given library
    extracted_files = extract_pdfs(args.pdf, args.recursive, args.extractor)

    api_callr = litellm_API_caller(
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

    # TODO Temp. Prompt
    prompt_path = Path("llm_api_caller") / "prompt.txt"
    prompt = prompt_path.read_text(encoding="utf-8")

    print("calling LLM...")
    # TODO call api with doc frome Extractor and safe the result
    result = api_callr.llm_call(prompt, extracted_files)

    # TODO save json

    # TODO print rep in the terminal
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
