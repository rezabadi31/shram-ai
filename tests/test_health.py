def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "ShramAI" in data["project"]
    assert data["docs"] == "/docs"


def test_health_check_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert data["services"]["document_ai"] == "ready"
    assert data["services"]["rule_engine"] == "ready"
    assert data["services"]["cross_document_anomaly"] == "ready"
    assert data["services"]["ml_risk_engine"] == "ready"
    assert data["services"]["agent_orchestrator"] == "ready"
    assert data["services"]["rag_retrieval"] == "ready"
