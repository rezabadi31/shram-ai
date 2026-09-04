from fastapi import APIRouter
from app.schemas.drift import (
    ModelDriftReport,
    RetrainTriggerRequest,
    RetrainTriggerResponse,
)
from app.ml.drift_monitor import DriftMonitorService

router = APIRouter()


@router.get("/report", response_model=ModelDriftReport)
def get_model_drift_report():
    """
    Retrieve comprehensive feature drift report, Population Stability Index (PSI),
    and inspector human-in-the-loop override statistics.
    """
    return DriftMonitorService.get_drift_report()


@router.post("/retrain", response_model=RetrainTriggerResponse)
def trigger_closed_loop_retraining(req: RetrainTriggerRequest):
    """
    Trigger closed-loop continuous ML retraining incorporating field inspection
    ground truth and human officer overrides. Promotes challenger if AUC improves.
    """
    return DriftMonitorService.trigger_closed_loop_retraining(req)
