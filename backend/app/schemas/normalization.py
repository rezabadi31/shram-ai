from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CanonicalRecordBase(BaseModel):
    employee_id: str
    employee_name: str
    source_document_id: str
    source_page: int = 1
    normalization_confidence: float = 0.95


class EmployeeRecord(CanonicalRecordBase):
    """Canonical schema for Form A - Register of Employees."""
    gender: Optional[str] = None
    designation: Optional[str] = None
    date_of_joining: Optional[str] = None
    uan: Optional[str] = None
    aadhaar_last4: Optional[str] = None
    esic_ip_number: Optional[str] = None
    department: Optional[str] = None
    skill_category: Optional[str] = None  # Unskilled, Semi-Skilled, Skilled, Highly Skilled


class WageRecord(CanonicalRecordBase):
    """Canonical schema for Form B - Register of Wages."""
    wage_period: str = "October 2024"
    daily_wage_rate: float
    days_worked: float
    basic_wage: float
    dearness_allowance: float = 0.0
    hra: float = 0.0
    overtime_hours: float = 0.0
    overtime_wages: float = 0.0
    gross_wages: float
    pf_deduction: float = 0.0
    esic_deduction: float = 0.0
    total_deductions: float = 0.0
    net_payable: float


class AttendanceRecord(CanonicalRecordBase):
    """Canonical schema for Form D - Muster Roll."""
    month: int = 10
    year: int = 2024
    days_present: float
    days_absent: float = 0.0
    paid_leaves: float = 0.0
    overtime_hours: float = 0.0
    total_mandays: float


class PayrollRecord(CanonicalRecordBase):
    """Canonical schema for Bank Payout Scroll."""
    bank_name: Optional[str] = "State Bank of India"
    account_number: Optional[str] = None
    ifsc: Optional[str] = None
    disbursed_amount: float
    transaction_reference: Optional[str] = None
    transaction_date: Optional[str] = None
    payment_status: str = "SUCCESS"


class MissingFieldFlag(BaseModel):
    field_name: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    affected_rows_count: int


class NormalizedDocumentDossier(BaseModel):
    document_id: str
    category: str
    record_type: str  # WAGE_RECORD, ATTENDANCE_RECORD, EMPLOYEE_RECORD, PAYROLL_RECORD
    records_count: int
    data_quality_score: float  # 0.0 to 1.0 (e.g. 0.94)
    normalization_confidence: float
    missing_fields: List[MissingFieldFlag] = Field(default_factory=list)
    records: List[Dict[str, Any]]
