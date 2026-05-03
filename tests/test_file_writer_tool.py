from tools.file_writer_tool import file_writer_tool


def test_file_writer_tool(tmp_path) -> None:
    file_path = tmp_path / "output.md"

    result = file_writer_tool(str(file_path), "Test content")

    assert result is True
    assert file_path.exists()
    assert file_path.read_text() == "Test content"
