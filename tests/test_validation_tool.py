from tools.validation_tool import validation_tool


def test_validation_tool_valid_output() -> None:
    output = """# Generated Implementation Plan

## Task 1: Build login API
- Implement the endpoint and request validation.
- Test success and failure paths.

## Task 2: Add error handling
- Implement exception middleware.
- Validate and monitor error responses.
"""

    result = validation_tool(output, expected_task_count=2)

    assert result["valid"] is True
    assert result["score"] >= 4
    assert result["checks"]["covers_tasks"] is True


def test_validation_tool_empty_output() -> None:
    result = validation_tool("")

    assert result["valid"] is False
    assert result["score"] == 0


def test_validation_tool_detects_dangerous_content() -> None:
    result = validation_tool("# Plan\n\nRun rm -rf / to clean up.")

    assert result["checks"]["safe_output"] is False
