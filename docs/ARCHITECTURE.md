# ShramAI Architecture & Technical Specification

## 1. Executive Overview
ShramAI is an end-to-end labour compliance intelligence platform designed to automate document audits, reconcile statutory registers, evaluate deterministic legal rules against the Four Labour Codes of India, identify cross-document anomalies, calculate explainable ML risk scores, and deliver actionable inspection briefs to labour inspectors.

## 2. Component Diagram

```text
+-----------------------------------------------------------------------------------+
|                                 FRONTEND LAYER                                    |
|  - Employer Portal (Self-audit, Document Center, Remediation)                     |
|  - Inspector Portal (Prioritized inspection queue, Risk distribution, Briefs)     |
|  - Demo Data Lab (Synthetic scenario testing: Compliant vs High-Risk)             |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (FastAPI)
                                           v
+-----------------------------------------------------------------------------------+
|                                 BACKEND LAYER                                     |
|                                                                                   |
|  [Document AI Engine]                                                             |
|   - Direct text extraction (PyMuPDF/PDFMiner) -> Fallback OCR (PaddleOCR)        |
|   - Layout and table extraction -> Structured JSON output                         |
|                                                                                   |
|  [Canonical Data Normalization]                                                   |
|   - Maps raw registers to standard schema with full source provenance             |
|                                                                                   |
|  [Agentic Orchestrator (LangGraph)]                                               |
|   - Document Agent: Confidence & completeness checks                              |
|   - Compliance Agent: Deterministic rule verification + Legal RAG retrieval       |
|   - Anomaly Agent: Cross-register discrepancies (headcount, payroll, attendance)  |
|   - Risk Agent: ML model invocation + SHAP explanation generation                 |
|   - Report Agent: Evidence-grounded inspection brief production                   |
|                                                                                   |
|  [Deterministic Rule Engine]                                                      |
|   - JSON rule catalogs (wage_rules.json, attendance_rules.json, etc.)             |
|   - Outputs: PASS, POTENTIAL COMPLIANCE ISSUE, INSUFFICIENT EVIDENCE              |
|                                                                                   |
|  [Labour Law RAG Engine]                                                          |
|   - Four Labour Codes (Wage, IR, Social Security, OSH&WC)                         |
|   - Vector retrieval with section, page, and official authority metadata          |
|                                                                                   |
|  [ML Risk Engine]                                                                 |
|   - Feature engineering pipeline (10+ multi-document signals)                     |
|   - Calibrated XGBoost classifier (Risk Score: 0 - 100)                           |
|   - TreeSHAP local explainability for inspector trust                             |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                                 STORAGE LAYER                                     |
|  - PostgreSQL: Canonical entities, findings, human feedback, audit logs           |
|  - pgvector / Chroma: Chunked statutory legal texts and embeddings               |
|  - Redis: Task queue, asynchronous document processing, agent session state       |
+-----------------------------------------------------------------------------------+
```

## 3. Data Contracts & Provenance Model
Every finding produced by ShramAI carries strict data provenance:
- `finding_id`: Unique UUID
- `establishment_id`: Establishment reference
- `rule_id`: Identifier of deterministic statutory rule
- `severity`: HIGH | MEDIUM | LOW
- `source_document`: File name and document type
- `page_number`: Target page containing evidence
- `extracted_evidence`: Structured snippet/data row that caused the flag
- `applicable_law`: Exact section and clause retrieved from Labour Codes
- `verification_status`: PENDING_VERIFICATION | CONFIRMED | REJECTED
