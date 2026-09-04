from typing import Optional
from fastapi import APIRouter, Body
from app.schemas.prioritization import (
    PrioritizationFilterParams,
    PrioritizedQueueResponse,
    InspectionScheduleBatchRequest,
    InspectionScheduleResponse,
    QueueSummaryMetrics,
)
from app.prioritization.queue_manager import InspectionQueueManager

router = APIRouter()


@router.post("/queue", response_model=PrioritizedQueueResponse, tags=["Inspection Prioritization"])
async def get_prioritized_inspection_queue(filters: Optional[PrioritizationFilterParams] = Body(default=None)):
    """
    Returns the multi-criteria risk-ranked inspection scheduling queue.
    Combines calibrated ML risk scores, anomaly density, recency penalties,
    and a 10% stratified randomized audit quota for fairness.
    """
    return InspectionQueueManager.get_prioritized_queue(filters)


@router.post("/schedule", response_model=InspectionScheduleResponse, tags=["Inspection Prioritization"])
async def schedule_inspection_batch(request: InspectionScheduleBatchRequest):
    """
    Batch schedules physical or desk inspections for designated establishments,
    allocates field inspector officers, and sets target audit deadlines.
    """
    return InspectionQueueManager.schedule_inspection_batch(request)


@router.get("/metrics", response_model=QueueSummaryMetrics, tags=["Inspection Prioritization"])
async def get_prioritization_queue_metrics():
    """
    Returns jurisdictional inspection capacity, priority distribution,
    and randomized control quota statistics.
    """
    return InspectionQueueManager.get_summary_metrics()
