def test_list_establishments(client):
    response = client.get("/api/v1/establishments")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    first = data[0]
    assert "name" in first
    assert "risk_score" in first
    assert "priority" in first


def test_get_establishment_dossier(client):
    response = client.get("/api/v1/establishments/EST-001")
    assert response.status_code == 200
    data = response.json()
    assert "establishment" in data
    assert "documents" in data
    assert "findings" in data
    assert "anomalies" in data
    assert "shap_contributions" in data
    assert "ai_inspection_brief" in data
    assert data["establishment"]["name"] == "ABC Industries Ltd."
    assert len(data["shap_contributions"]) >= 3
