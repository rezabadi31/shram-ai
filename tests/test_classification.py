from app.document_ai.document_classifier import DocumentClassifierService
from app.schemas.classification import ClassifiedCategory, ClassifierStage


def test_classify_wage_register_rule_heuristics():
    text = "FORM B - REGISTER OF WAGES [Rule 78(1)(a)(i)]\nEstablishment: ABC Industries\nWage Rate | Net Payable"
    result = DocumentClassifierService.classify(text, filename="register.pdf")
    assert result.predicted_category == ClassifiedCategory.WAGE_REGISTER
    assert result.confidence >= 0.95
    assert result.classifier_stage == ClassifierStage.RULE_HEURISTICS
    assert len(result.matched_signals) >= 1


def test_classify_attendance_register_rule_heuristics():
    text = "FORM D - MUSTER ROLL [Rule 78(1)(a)(ii)]\nMonth of October 2024\nDays Worked | Shift Timing"
    result = DocumentClassifierService.classify(text, filename="attendance_oct.pdf")
    assert result.predicted_category == ClassifiedCategory.ATTENDANCE_REGISTER
    assert result.confidence >= 0.95
    assert result.classifier_stage == ClassifierStage.RULE_HEURISTICS


def test_classify_employee_register_rule_heuristics():
    text = "FORM A - REGISTER OF EMPLOYEES\nUniversal Account Number UAN | EPFO Member ID | Date of Joining"
    result = DocumentClassifierService.classify(text, filename="form_a.pdf")
    assert result.predicted_category == ClassifiedCategory.EMPLOYEE_REGISTER
    assert result.confidence >= 0.95


def test_classify_payroll_bank_scroll():
    text = "Bank Payout Scroll - Salary Disbursement Advice\nNEFT Transaction UTR Number | Beneficiary Account"
    result = DocumentClassifierService.classify(text, filename="salary_scroll.pdf")
    assert result.predicted_category == ClassifiedCategory.PAYROLL
    assert result.confidence >= 0.90


def test_classify_ml_fallback():
    # Degraded text without strict Form B regex, using general wage terminology
    text = "monthly remuneration calculation breakdown base salary stipend reimbursement per diem payment for services rendered in plant unit"
    result = DocumentClassifierService.classify(text, filename="scan_page_3.png")
    assert result.predicted_category == ClassifiedCategory.WAGE_REGISTER
    assert result.classifier_stage == ClassifierStage.ML_FALLBACK
    assert result.confidence >= 0.50


def test_classify_unknown_text():
    text = "The weather today in New Delhi is clear and sunny with light winds."
    result = DocumentClassifierService.classify(text, filename="random_notes.txt")
    assert result.predicted_category == ClassifiedCategory.UNKNOWN
    assert result.confidence <= 0.50


def test_classify_endpoint(client):
    response = client.post(
        "/api/v1/documents/classify-text",
        json={
            "text": "Safety Committee Minutes and Factory Inspection Report Form 18",
            "filename": "safety_minutes.pdf",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_category"] == "Safety Record"
    assert data["confidence"] >= 0.90
