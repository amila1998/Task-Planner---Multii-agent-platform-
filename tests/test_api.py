from fastapi.testclient import TestClient

from agents.code_generation_agent import CodeGenerationAgent
import api as api_module
from api import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_workflow_run_endpoint_with_mocked_ollama(monkeypatch) -> None:
    mocked_output = """# Generated Implementation Plan

## Task 1: Build feature
- Implement endpoint.
- Test behavior.

## Task 2: Validate feature
- Implement validation checks.
- Test negative paths.
"""

    monkeypatch.setattr(
        CodeGenerationAgent,
        "_generate_with_ollama",
        lambda self, prompt: mocked_output,
    )

    response = client.post(
        "/workflow/run",
        json={
            "requirement": "Build feature and validate feature",
            "fallback_to_template": False,
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["workflow"]["status"] == "completed"
    assert payload["workflow"]["generation_source"] == "ollama"


def test_workflow_run_endpoint_passes_timeout(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_execute_workflow(**kwargs):
        captured.update(kwargs)
        return {
            "user_input": kwargs["user_input"],
            "planned_tasks": [],
            "generated_output": None,
            "validation_result": None,
            "generation_source": None,
            "status": "failed",
            "errors": [],
        }

    monkeypatch.setattr(api_module, "execute_workflow", fake_execute_workflow)

    response = client.post(
        "/workflow/run",
        json={
            "requirement": "Build feature and validate feature",
            "ollama_timeout_seconds": 240,
        },
    )

    assert response.status_code == 200
    assert captured["ollama_timeout_seconds"] == 240
