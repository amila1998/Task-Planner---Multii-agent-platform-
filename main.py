import logging
from pathlib import Path
from typing import Optional

from agents.code_generation_agent import CodeGenerationAgent
from agents.coordinator_agent import CoordinatorAgent
from agents.task_planning_agent import TaskPlanningAgent
from agents.validation_agent import ValidationAgent
from tools.file_writer_tool import file_writer_tool
from state.workflow_state import WorkflowState

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/agent_execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def execute_workflow(
    user_input: str,
    ollama_model: str = "llama3",
    ollama_base_url: str = "http://localhost:11434",
    fallback_to_template: bool = True,
    output_path: Optional[str] = "outputs/generated_plan.md",
) -> WorkflowState:
    """Run the full multi-agent workflow and return the final state."""

    coordinator = CoordinatorAgent()
    planner = TaskPlanningAgent()
    generator = CodeGenerationAgent(
        model=ollama_model,
        ollama_base_url=ollama_base_url,
        fallback_to_template=fallback_to_template,
    )
    validator = ValidationAgent()

    state = coordinator.run(user_input)

    if state["status"] == "failed":
        state["generation_source"] = None
        return state

    state["generation_source"] = None

    state = planner.run(state)
    if state["status"] == "failed":
        return state

    state = generator.run(state)
    if state["status"] == "failed":
        return state

    state = validator.run(state)

    if state["generated_output"] and output_path:
        file_writer_tool(output_path, state["generated_output"])

    return state


def run_mas(user_input: str) -> None:
    """Run workflow and print final state for CLI usage."""

    state = execute_workflow(user_input)

    print("Final State:")
    print(state)


if __name__ == "__main__":
    requirement = "Build a login system with validation and error handling"
    run_mas(requirement)
