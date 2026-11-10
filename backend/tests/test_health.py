"""HTTP smoke tests."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_returns_healthy() -> None:
    """The health endpoint reports process liveness."""
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_agent_execution_simulation() -> None:
    """The demo endpoint returns a structured simulated result."""
    with TestClient(create_app()) as client:
        response = client.post(
            "/api/v1/agent/execute",
            json={"tenant_id": 1, "agent_id": 2, "prompt": "Review this code"},
        )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["tenant_id"] == 1
