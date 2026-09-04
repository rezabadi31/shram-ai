from app.agents.graph import OrchestratorService, build_shram_audit_graph
from app.schemas.agent_state import WorkflowStatus


def test_shram_orchestrator_graph_compilation():
    compiled = build_shram_audit_graph()
    assert compiled is not None


def test_agent_orchestrator_execution():
    result = OrchestratorService.execute_audit("EST-001")
    assert result["workflow_id"].startswith("WF-")
    assert result["status"] == WorkflowStatus.COMPLETED.value
    assert result["steps_completed"] >= 5

    # Check deterministic boundaries
    assert result["compliance_score"] > 0.0
    assert result["risk_score"] > 0.0
    assert result["risk_category"] in ["HIGH", "MEDIUM", "LOW"]
    assert result["findings_count"] >= 1

    # Verify AI brief structure
    brief = result["ai_inspection_brief"]
    assert "summary" in brief
    assert len(brief["critical_focus_areas"]) >= 2
    assert len(brief["recommended_documents"]) >= 2


def test_agent_orchestrator_api_endpoints(client):
    # Test POST orchestrate
    response = client.post("/api/v1/agents/orchestrate?establishment_id=EST-001")
    assert response.status_code == 200
    data = response.json()
    assert data["workflow_id"].startswith("WF-")
    assert data["status"] == "COMPLETED"
    assert data["steps_completed"] >= 5
    assert len(data["steps"]) >= 5

    # Test GET status
    wf_id = data["workflow_id"]
    status_response = client.get(f"/api/v1/agents/status/{wf_id}")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["workflow_id"] == wf_id
