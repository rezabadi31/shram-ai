from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    establishments,
    auth,
    documents,
    extraction,
    classification,
    normalization,
    knowledge,
    rag,
    compliance,
    agents,
    document_agent,
    compliance_agent,
    risk_agent,
    anomalies,
    evidence_graph,
    dataset,
    features,
    models,
    shap,
    prioritization,
    explanation,
    employer,
    inspection,
    timeline,
    notices,
    drift,
    analytics,
    reports,
    deployment,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(establishments.router, prefix="/establishments")
api_router.include_router(documents.router, prefix="/documents")
api_router.include_router(extraction.router, prefix="/documents")
api_router.include_router(classification.router, prefix="/documents")
api_router.include_router(normalization.router, prefix="/documents")
api_router.include_router(knowledge.router, prefix="/knowledge")
api_router.include_router(rag.router, prefix="/rag")
api_router.include_router(compliance.router, prefix="/compliance")
api_router.include_router(agents.router, prefix="/agents")
api_router.include_router(document_agent.router, prefix="/agents/document")
api_router.include_router(compliance_agent.router, prefix="/agents/compliance")
api_router.include_router(risk_agent.router, prefix="/agents/risk")
api_router.include_router(anomalies.router, prefix="/anomalies")
api_router.include_router(evidence_graph.router, prefix="/evidence-graph")
api_router.include_router(dataset.router, prefix="/dataset")
api_router.include_router(features.router, prefix="/ml/features")
api_router.include_router(models.router, prefix="/ml/models")
api_router.include_router(shap.router, prefix="/ml/shap")
api_router.include_router(prioritization.router, prefix="/prioritization")
api_router.include_router(explanation.router, prefix="/explanation")
api_router.include_router(employer.router, prefix="/employer")
api_router.include_router(inspection.router, prefix="/inspection")
api_router.include_router(timeline.router, prefix="/establishments")
api_router.include_router(notices.router, prefix="/notices")
api_router.include_router(drift.router, prefix="/ml/drift")
api_router.include_router(analytics.router, prefix="/analytics")
api_router.include_router(reports.router, prefix="/reports")
api_router.include_router(deployment.router, prefix="/deployment")

