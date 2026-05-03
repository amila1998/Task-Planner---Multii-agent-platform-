from typing import Any, Dict, List, Optional, TypedDict


class WorkflowState(TypedDict):
    """Shared global state passed between all agents."""

    user_input: str
    planned_tasks: List[Dict[str, Any]]
    generated_output: Optional[str]
    validation_result: Optional[Dict[str, Any]]
    generation_source: Optional[str]
    status: str
    errors: List[str]
