from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from main import execute_workflow


app = FastAPI(title="Multi-Agent Workflow API", version="1.0.0")


class WorkflowRequest(BaseModel):
    requirement: str = Field(..., min_length=1)
    model: str = Field(default="llama3")
    ollama_base_url: str = Field(default="http://localhost:11434")
    fallback_to_template: bool = Field(default=True)
    ollama_timeout_seconds: int = Field(default=180, ge=1)


class WorkflowResponse(BaseModel):
    workflow: Dict[str, Any]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/workflow/run", response_model=WorkflowResponse)
def run_workflow(request: WorkflowRequest) -> WorkflowResponse:
    if not request.requirement.strip():
        raise HTTPException(status_code=400, detail="Requirement cannot be empty")

    state = execute_workflow(
        user_input=request.requirement,
        ollama_model=request.model,
        ollama_base_url=request.ollama_base_url,
        fallback_to_template=request.fallback_to_template,
        ollama_timeout_seconds=request.ollama_timeout_seconds,
        output_path="outputs/generated_plan_api.md",
    )

    return WorkflowResponse(workflow=state)
