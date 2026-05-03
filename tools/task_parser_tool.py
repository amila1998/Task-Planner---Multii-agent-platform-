from typing import Dict, List


def task_parser_tool(requirement: str) -> List[Dict[str, str]]:
    """Parse a raw requirement into structured tasks."""

    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty")

    normalized_text = (
        requirement.replace(" and ", ".").replace(",", ".").replace(";", ".")
    )

    parts = normalized_text.split(".")
    tasks: List[Dict[str, str]] = []

    for index, part in enumerate(parts, start=1):
        clean_task = part.strip()
        if clean_task:
            tasks.append(
                {
                    "id": str(index),
                    "title": clean_task.capitalize(),
                    "description": f"Complete: {clean_task}",
                }
            )

    return tasks
