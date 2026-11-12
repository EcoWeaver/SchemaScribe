from errors import UserError
from extractor.loader import load_extractor


def extract_pdfs(paths, search_recursive, library):
    # iterate over all files to collect all files from directories
    pdf_files = resolve_paths(paths, search_recursive)

    # load library
    extractor = load_extractor(library)
    print(f"\nStarting extraction of {len(pdf_files)} PDF(s) with {library}  ...")

    # for later: use a data structure with more information
    # (like original file name, pages, ...)
    converted_files = {}
    failed_files = []
    for file_path in pdf_files:
        try:
            converted_files[file_path.name] = extractor.to_markdown(file_path)
            print(f"  - Successfully converted <{file_path.name}> to Markdown ...")
        except Exception as e:
            failed_files.append((file_path, e))
            print(f"  - Warning: failed to process <{file_path.name}> ")

    if failed_files:
        print(f"\nFailed to convert {len(failed_files)} files!")

        # could save results as .md file here if needed

    return converted_files


def resolve_paths(raw_paths, search_recursive):
    # use set to eliminate duplicates when searching directories
    file_paths = set()
    invalid_paths = set()
    glob_pattern = "**/*.pdf" if search_recursive else "*.pdf"

    # collect pdf files from directory paths
    for path in raw_paths:
        if path.is_dir():
            for file in path.glob(glob_pattern):
                if file.is_file():
                    file_paths.add(file.resolve())
        else:
            # if file type is different from pdf, dont process it
            if path.suffix.lower() == ".pdf":
                file_paths.add(path.resolve())
            else:
                invalid_paths.add(path.resolve())

    if invalid_paths:
        print(
            "\nWarning: The following paths are not PDF files "
            "and will not be processed:"
        )
        for path in invalid_paths:
            print(f"  - {path}")

    # abort program if no valid files coudld be found
    if not file_paths:
        raise UserError("None of the provided paths point to valid PDF files.")

    # could be list(file_paths) if order is not that important
    return sorted(file_paths)
