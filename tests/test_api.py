from fastapi.testclient import TestClient

from agents.code_generation_agent import CodeGenerationAgent
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
