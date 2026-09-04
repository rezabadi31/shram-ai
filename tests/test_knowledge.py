from app.rag.ingestion import KnowledgeBaseService


def test_knowledge_base_loading():
    codes = KnowledgeBaseService.list_codes()
    assert len(codes) == 4
    code_ids = {c.code_id for c in codes}
    assert "wages_2019" in code_ids
    assert "ir_2020" in code_ids
    assert "ss_2020" in code_ids
    assert "oshwc_2020" in code_ids


def test_get_exact_statutory_section():
    sec14 = KnowledgeBaseService.get_section("wages_2019", "14")
    assert sec14 is not None
    assert sec14.title == "Wages for Overtime Work"
    assert "twice the normal rate" in sec14.statutory_text
    assert sec14.penalties is not None
    assert sec14.citation == "The Code on Wages, 2019, Sec. 14"


def test_search_knowledge_by_keyword():
    result = KnowledgeBaseService.search_sections("safety committee")
    assert result.total_matches >= 1
    top_match = result.results[0]
    assert "Safety Committee" in top_match.title
    assert top_match.code_id == "oshwc_2020"


def test_knowledge_api_codes_endpoint(client):
    response = client.get("/api/v1/knowledge/codes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    first = data[0]
    assert "code_id" in first
    assert "mandatory_registers" in first


def test_knowledge_api_code_details_endpoint(client):
    response = client.get("/api/v1/knowledge/codes/wages_2019")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["code_id"] == "wages_2019"
    assert len(data["sections"]) >= 4


def test_knowledge_api_search_endpoint(client):
    response = client.get("/api/v1/knowledge/search?q=overtime")
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] >= 1
    assert any("Overtime" in s["title"] or "overtime" in s["keywords"] for s in data["results"])
