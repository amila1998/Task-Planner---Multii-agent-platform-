import logging

from state.workflow_state import WorkflowState


class CoordinatorAgent:
    """Initialize workflow state from user input."""

    def __init__(self, name: str = "Coordinator Agent") -> None:
        self.name = name

    def run(self, user_input: str) -> WorkflowState:
        logging.info("[%s] Received user input", self.name)

        if not user_input or not user_input.strip():
            return {
                "user_input": user_input,
                "planned_tasks": [],
                "generated_output": None,
                "validation_result": None,
                "status": "failed",
                "errors": ["User input cannot be empty"],
            }

        return {
            "user_input": user_input,
            "planned_tasks": [],
            "generated_output": None,
            "validation_result": None,
            "status": "received",
            "errors": [],
        }
