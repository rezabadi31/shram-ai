from app.anomaly.cross_reconciler import CrossDocumentAnomalyEngine
from app.schemas.anomaly import AnomalyType, AnomalySeverity


def test_ghost_worker_detection():
    wages = [{"employee_id": "EMP-999", "employee_name": "Ghost User", "gross_wages": 18000.0, "total_deductions": 0.0}]
    attendance = [{"employee_id": "EMP-999", "days_present": 0}]
    anomalies = CrossDocumentAnomalyEngine.reconcile_wages_and_attendance(wages, attendance)
    assert len(anomalies) == 1
    assert anomalies[0].anomaly_type == AnomalyType.GHOST_WORKER
    assert anomalies[0].severity == AnomalySeverity.HIGH
    assert anomalies[0].affected_worker_id == "EMP-999"


def test_uncompensated_attendance_detection():
    wages = []
    attendance = [{"employee_id": "EMP-888", "employee_name": "Unpaid Worker", "days_present": 25}]
    anomalies = CrossDocumentAnomalyEngine.reconcile_wages_and_attendance(wages, attendance)
    assert len(anomalies) == 1
    assert anomalies[0].anomaly_type == AnomalyType.UNCOMPENSATED_ATTENDANCE
    assert anomalies[0].affected_worker_id == "EMP-888"


def test_bank_disbursement_mismatch():
    wages = [{"employee_id": "EMP-001", "employee_name": "Ramesh", "gross_wages": 20000.0, "total_deductions": 2000.0}]  # Expected net = 18000
    bank = [{"employee_id": "EMP-001", "amount": 16500.0}]  # Discrepancy: ₹1,500
    anomalies = CrossDocumentAnomalyEngine.reconcile_wages_and_bank(wages, bank)
    assert len(anomalies) == 1
    assert anomalies[0].anomaly_type == AnomalyType.DISBURSEMENT_MISMATCH
    assert anomalies[0].discrepancy_amount == 1500.0


def test_contractor_suppression_detection():
    anomalies = CrossDocumentAnomalyEngine.reconcile_contract_headcount(gate_muster_count=450, statutory_register_count=400)
    assert len(anomalies) == 1
    assert anomalies[0].anomaly_type == AnomalyType.CONTRACTOR_SUPPRESSION
    assert "50 undeclared" in anomalies[0].description


def test_full_establishment_reconciliation():
    result = CrossDocumentAnomalyEngine.run_establishment_reconciliation(establishment_id="EST-001")
    assert result.establishment_id == "EST-001"
    assert result.reconciliation_summary.anomalies_detected >= 3
    assert result.reconciliation_summary.ghost_workers_count >= 1
    assert result.reconciliation_summary.uncompensated_workers_count >= 1
    assert result.reconciliation_summary.financial_discrepancy_total > 0
    assert len(result.recommendations) >= 2


def test_anomaly_api_endpoints(client):
    # GET types
    types_resp = client.get("/api/v1/anomalies/types")
    assert types_resp.status_code == 200
    assert len(types_resp.json()) >= 4

    # POST reconcile
    rec_resp = client.post("/api/v1/anomalies/reconcile?establishment_id=EST-001")
    assert rec_resp.status_code == 200
    data = rec_resp.json()
    assert data["establishment_id"] == "EST-001"
    assert "reconciliation_summary" in data
    assert len(data["anomalies"]) >= 3
