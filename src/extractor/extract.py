def extract_pdfs(paths, search_recursive, library):
    # iterate over all files to collect all files from directories
    pdf_files = resolve_paths(paths, search_recursive)
    print(pdf_files)

    # load library
    print(library)


def resolve_paths(raw_paths, search_recursive):
    # use set to eliminate duplicates when searching directories
    file_paths = set()
    glob_pattern = "**/*.pdf" if search_recursive else "*.pdf"

    for path in raw_paths:
        if path.is_dir():
            for file in path.glob(glob_pattern):
                if file.is_file():
                    file_paths.add(file.resolve())
        else:
            file_paths.add(path.resolve())

    # could be list(file_paths) if order is not that important
    return sorted(file_paths)
