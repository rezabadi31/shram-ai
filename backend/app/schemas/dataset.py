from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class EstablishmentRecordSynthetic(BaseModel):
    establishment_id: str
    name: str
    state: str
    district: str
    industry_sector: str
    hazardous_process: bool
    worker_count: int
    contract_worker_ratio: float
    female_worker_ratio: float
    wage_violation_count: int
    ot_violation_count: int
    deduction_violation_count: int
    missing_register_count: int
    ghost_worker_count: int
    uncompensated_worker_count: int
    disbursement_mismatch_count: int
    inspection_history_violations: int
    grievance_complaint_count: int
    ground_truth_risk_score: float
    ground_truth_inspection_priority: str  # HIGH, MEDIUM, LOW


class DatasetGenerationConfig(BaseModel):
    num_samples: int = Field(default=1000, ge=10, le=10000)
    seed: Optional[int] = 42
    save_to_disk: bool = True


class SectorDistributionItem(BaseModel):
    sector: str
    count: int
    percentage: float


class RiskDistributionItem(BaseModel):
    priority: str
    count: int
    percentage: float


class DatasetSummaryMetrics(BaseModel):
    total_establishments: int
    average_worker_count: float
    average_risk_score: float
    sector_distribution: List[SectorDistributionItem]
    risk_distribution: List[RiskDistributionItem]
    total_violations_simulated: int
    total_ghost_workers_simulated: int


class DatasetGenerationResponse(BaseModel):
    status: str
    samples_generated: int
    csv_path: Optional[str] = None
    json_path: Optional[str] = None
    summary_metrics: DatasetSummaryMetrics
