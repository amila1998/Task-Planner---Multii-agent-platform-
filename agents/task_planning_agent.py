import logging

from state.workflow_state import WorkflowState
from tools.task_parser_tool import task_parser_tool


class TaskPlanningAgent:
    """Convert user requirement into structured tasks."""

    def __init__(self, name: str = "Task Planning Agent") -> None:
        self.name = name

    def run(self, state: WorkflowState) -> WorkflowState:
        logging.info("[%s] Started task planning", self.name)

        try:
            tasks = task_parser_tool(state["user_input"])
            state["planned_tasks"] = tasks
            state["status"] = "planned"
            logging.info("[%s] Planned %s tasks", self.name, len(tasks))
        except Exception as error:  # pylint: disable=broad-exception-caught
            state["status"] = "failed"
            state["errors"].append(str(error))
            logging.error("[%s] Error: %s", self.name, error)

        return state
