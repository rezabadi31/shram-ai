from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ClassifiedCategory(str, Enum):
    WAGE_REGISTER = "Wage Register"
    ATTENDANCE_REGISTER = "Attendance Register"
    EMPLOYEE_REGISTER = "Employee Register"
    PAYROLL = "Payroll"
    SAFETY_RECORD = "Safety Record"
    EMPLOYMENT_CONTRACT = "Employment Contract"
    RETURN = "Return"
    UNKNOWN = "Unknown"


class ClassifierStage(str, Enum):
    RULE_HEURISTICS = "RULE_HEURISTICS"
    ML_FALLBACK = "ML_FALLBACK"


class ClassificationMatchSignal(BaseModel):
    signal_name: str
    matched_pattern: str
    weight: float


class ClassificationResult(BaseModel):
    document_id: Optional[str] = None
    predicted_category: ClassifiedCategory
    confidence: float
    classifier_stage: ClassifierStage
    matched_signals: List[ClassificationMatchSignal]
    alternative_candidates: List[dict] = Field(default_factory=list)


class TextClassificationRequest(BaseModel):
    text: str
    filename: Optional[str] = None
