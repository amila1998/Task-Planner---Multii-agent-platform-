from langgraph.graph import END, StateGraph

from agents.code_generation_agent import CodeGenerationAgent
from agents.task_planning_agent import TaskPlanningAgent
from agents.validation_agent import ValidationAgent
from state.workflow_state import WorkflowState

planner = TaskPlanningAgent()
generator = CodeGenerationAgent()
validator = ValidationAgent()


def planning_node(state: WorkflowState) -> WorkflowState:
    return planner.run(state)


def generation_node(state: WorkflowState) -> WorkflowState:
    return generator.run(state)


def validation_node(state: WorkflowState) -> WorkflowState:
    return validator.run(state)


graph = StateGraph(WorkflowState)

graph.add_node("planning", planning_node)
graph.add_node("generation", generation_node)
graph.add_node("validation", validation_node)

graph.set_entry_point("planning")
graph.add_edge("planning", "generation")
graph.add_edge("generation", "validation")
graph.add_edge("validation", END)

app = graph.compile()

initial_state: WorkflowState = {
    "user_input": "Build a login system with validation and error handling",
    "planned_tasks": [],
    "generated_output": None,
    "validation_result": None,
    "status": "received",
    "errors": [],
}

if __name__ == "__main__":
    result = app.invoke(initial_state)
    print(result)
