from agents.code_generation_agent import CodeGenerationAgent
from main import execute_workflow


def test_ollama_request_uses_configured_timeout(monkeypatch) -> None:
    agent = CodeGenerationAgent(request_timeout_seconds=240)
    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return b'{"response": "# Generated Implementation Plan"}'

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("agents.code_generation_agent.urlopen", fake_urlopen)

    output = agent._generate_with_ollama("test prompt")

    assert output == "# Generated Implementation Plan"
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["timeout"] == 240


def test_execute_workflow_with_mocked_ollama(monkeypatch) -> None:
    mocked_output = """# Generated Implementation Plan

## Task 1: Build login flow
- Implement API endpoint and input validation.
- Test valid and invalid credentials.

## Task 2: Add robust error handling
- Implement exception mapping and safe responses.
- Validate logs and monitoring hooks.
"""

    monkeypatch.setattr(
        CodeGenerationAgent,
        "_generate_with_ollama",
        lambda self, prompt: mocked_output,
    )

    state = execute_workflow(
        user_input="Build login flow and add robust error handling",
        fallback_to_template=False,
        output_path=None,
    )

    assert state["status"] == "completed"
    assert state["generation_source"] == "ollama"
    assert state["generated_output"] is not None
    assert state["validation_result"] is not None
    assert state["validation_result"]["valid"] is True
