from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class JurisdictionMetric(BaseModel):
    jurisdiction_id: str
    jurisdiction_name: str
    sphere: str  # CENTRAL | STATE
    total_establishments: int
    audited_count: int
    high_risk_count: int
    average_risk_score: float
    compliance_rate_pct: float
    arrears_recovered_inr: float
    notices_issued_count: int


class SectorRiskMetric(BaseModel):
    sector_id: str
    sector_name: str
    hazard_tier: str  # HIGH_HAZARD | MEDIUM_HAZARD | LOW_HAZARD
    total_units: int
    non_compliance_rate_pct: float
    top_violation_code: str
    estimated_underpayment_inr: float


class MonthlyTrendPoint(BaseModel):
    month: str
    audits_completed: int
    violations_detected: int
    safe_harbour_achieved: int
    compliance_index: float


class MacroOverviewResponse(BaseModel):
    national_compliance_index: float
    total_registered_workforce: int
    total_active_establishments: int
    total_inspections_scheduled_quarter: int
    total_penalties_assessed_inr: float
    total_arrears_recovered_inr: float
    safe_harbour_achieved_count: int
    jurisdictions: List[JurisdictionMetric]
    sectors: List[SectorRiskMetric]
    monthly_trend: List[MonthlyTrendPoint]
    metadata: Optional[Dict[str, Any]] = None
