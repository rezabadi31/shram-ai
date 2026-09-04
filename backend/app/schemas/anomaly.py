from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnomalyType(str, Enum):
    GHOST_WORKER = "GHOST_WORKER"
    UNCOMPENSATED_ATTENDANCE = "UNCOMPENSATED_ATTENDANCE"
    DISBURSEMENT_MISMATCH = "DISBURSEMENT_MISMATCH"
    OVERTIME_HOURS_DISCREPANCY = "OVERTIME_HOURS_DISCREPANCY"
    CONTRACTOR_SUPPRESSION = "CONTRACTOR_SUPPRESSION"


class AnomalySeverity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CrossDocumentAnomalyItem(BaseModel):
    anomaly_id: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    primary_document: str
    cross_reference_document: str
    description: str
    discrepancy_amount: Optional[float] = None
    affected_worker_id: Optional[str] = None
    affected_worker_name: Optional[str] = None
    statutory_implication: str


class ReconciliationSummary(BaseModel):
    records_reconciled: int
    anomalies_detected: int
    financial_discrepancy_total: float
    ghost_workers_count: int
    uncompensated_workers_count: int


class CrossDocumentAuditResult(BaseModel):
    establishment_id: str
    audit_timestamp: str
    reconciliation_summary: ReconciliationSummary
    anomalies: List[CrossDocumentAnomalyItem]
    recommendations: List[str]
