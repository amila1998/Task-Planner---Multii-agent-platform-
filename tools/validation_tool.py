import re
from typing import Any, Dict


def validation_tool(output: str, expected_task_count: int = 0) -> Dict[str, Any]:
    """Validate generated output with quality, completeness, and safety checks."""

    if not output or not output.strip():
        return {"valid": False, "score": 0, "message": "Output is empty"}

    lowered = output.lower()

    task_mentions = len(re.findall(r"^##\s+task\s+\d+", output, flags=re.IGNORECASE | re.MULTILINE))

    dangerous_patterns = [
        r"rm\s+-rf",
        r"del\s+/f\s+/s\s+/q",
        r"drop\s+database",
        r"shutdown\s+-s",
        r"format\s+c:",
        r"delete\s+all",
    ]

    checks = {
        "has_content": len(output.strip()) > 0,
        "has_markdown_structure": output.strip().startswith("#") and "##" in output,
        "has_actionability": any(
            keyword in lowered
            for keyword in ["implement", "test", "validate", "api", "deploy", "monitor"]
        ),
        "sufficient_detail": len(output.strip()) >= 180,
        "covers_tasks": expected_task_count == 0 or task_mentions >= expected_task_count,
        "safe_output": not any(re.search(pattern, lowered) for pattern in dangerous_patterns),
    }

    score = sum(1 for value in checks.values() if value)
    max_score = len(checks)

    failed_checks = [name for name, passed in checks.items() if not passed]

    return {
        "valid": score >= 4,
        "score": score,
        "max_score": max_score,
        "checks": checks,
        "failed_checks": failed_checks,
        "task_mentions": task_mentions,
        "message": "Validation completed",
    }
