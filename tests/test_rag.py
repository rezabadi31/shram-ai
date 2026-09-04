from app.rag.retrieval import HybridRetriever
from app.schemas.rag import RAGRetrievalMode


def test_keyword_retrieval_exact_section():
    results = HybridRetriever.keyword_search("Section 14 overtime", top_k=3)
    assert len(results) >= 1
    top_chunk, score = results[0]
    assert "Section 14" in top_chunk.metadata["section_number"]
    assert score > 0.5


def test_semantic_retrieval_concept():
    # Conceptual question without exact statute title
    results = HybridRetriever.semantic_search("how many hours can an employee work in a factory each day?", top_k=3)
    assert len(results) >= 1
    top_chunk, score = results[0]
    # Should match Section 25 (Daily and Weekly Working Hours)
    assert "25" in top_chunk.metadata["section_number"] or "hours" in top_chunk.text.lower()


def test_hybrid_rrf_retrieval():
    results = HybridRetriever.hybrid_search_rrf("safety committee hazardous factory", top_k=3)
    assert len(results) >= 1
    top_chunk, score = results[0]
    assert "Section 22" in top_chunk.metadata["section_number"]
    assert "Safety Committee" in top_chunk.metadata["title"]


def test_zero_hallucination_verification(client):
    # Test query against RAG endpoint
    response = client.post(
        "/api/v1/rag/query",
        json={"query": "What is the penalty for not paying minimum wages?", "mode": "HYBRID"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["zero_hallucination_verified"] is True
    assert len(data["citations"]) >= 1

    citation = data["citations"][0]
    # Must cite Code on Wages Section 6 or 8
    assert citation["code_id"] == "wages_2019"
    assert citation["section_number"] in ["Section 6", "Section 8"]
    assert "50,000" in citation["citation_text"] or citation["penalty_summary"] is not None


def test_rag_query_unrelated_query(client):
    response = client.post(
        "/api/v1/rag/query",
        json={"query": "xyz123 quantum black hole astrophysics", "mode": "KEYWORD"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "No authoritative statutory provision found" in data["answer"]
    assert len(data["citations"]) == 0
