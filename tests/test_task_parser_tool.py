import pytest

from tools.task_parser_tool import task_parser_tool


def test_task_parser_tool_success() -> None:
    result = task_parser_tool("Build login system. Add validation.")

    assert len(result) == 2
    assert result[0]["title"] == "Build login system"
    assert result[1]["title"] == "Add validation"


def test_task_parser_tool_empty_input() -> None:
    with pytest.raises(ValueError):
        task_parser_tool("")
