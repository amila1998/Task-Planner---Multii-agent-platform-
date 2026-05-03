from pathlib import Path


def file_writer_tool(file_path: str, content: str) -> bool:
    """Write generated content to a file path."""

    if not file_path or not file_path.strip():
        raise ValueError("File path cannot be empty")

    if content is None:
        raise ValueError("Content cannot be None")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return True
