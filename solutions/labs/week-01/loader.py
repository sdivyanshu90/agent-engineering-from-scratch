from pathlib import Path


def load_texts(root):
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(str(root))
    result = []
    for path in sorted(root.iterdir()):
        if path.is_file() and path.suffix == ".txt":
            result.append((path.name, path.read_text(encoding="utf-8")))
    return result
