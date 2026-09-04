from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.agent_state import OrchestrationExecutionResponse
from app.agents.graph import OrchestratorService

router = APIRouter()


@router.post("/orchestrate", response_model=OrchestrationExecutionResponse, tags=["Agentic AI Orchestrator"])
async def run_agentic_audit(
    establishment_id: str = Query("EST-001", description="Target establishment ID to audit"),
):
    """
    Triggers the LangGraph multi-agent orchestration state machine.
    Coordinates Document Agent, Compliance Agent, Risk Agent, and Explanation Node with deterministic guardrails.
    """
    result = OrchestratorService.execute_audit(establishment_id)
    return result


@router.get("/status/{workflow_id}", tags=["Agentic AI Orchestrator"])
async def get_workflow_status(workflow_id: str):
    """Returns execution state and agent execution log for a workflow run."""
    state = OrchestratorService.get_workflow_status(workflow_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow '{workflow_id}' not found",
        )
    return state
