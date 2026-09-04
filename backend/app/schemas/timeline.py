import datetime
from typing import List, Optional
from pydantic import BaseModel


class TimelineEvent(BaseModel):
    event_id: str
    event_type: str
    # EVENT TYPES:
    # DOCUMENT_SUBMITTED, COMPLIANCE_EVALUATED, RISK_ASSESSED,
    # ANOMALY_DETECTED, INSPECTION_SCHEDULED, VIOLATION_DETECTED,
    # REMEDIATION_SUBMITTED, NOTICE_ISSUED, PENALTY_PROPOSED, SAFE_HARBOUR_ACHIEVED
    timestamp: str
    date_label: str
    actor: str
    actor_type: str  # EMPLOYER | INSPECTOR | SYSTEM | ML_ENGINE
    title: str
    description: str
    severity: str  # INFO | LOW | MEDIUM | HIGH | CRITICAL
    metadata: Optional[dict] = None


class EstablishmentTimeline(BaseModel):
    establishment_id: str
    establishment_name: str
    total_events: int
    first_audit_date: str
    last_activity_date: str
    events: List[TimelineEvent]
