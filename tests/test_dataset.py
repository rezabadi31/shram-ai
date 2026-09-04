import os
from pathlib import Path
from app.dataset.generator import SyntheticDatasetGenerator


def test_synthetic_dataset_generation():
    response = SyntheticDatasetGenerator.generate_dataset(num_samples=100, seed=123, save_to_disk=True)
    assert response.status == "SUCCESS"
    assert response.samples_generated == 100
    assert response.csv_path is not None
    assert response.json_path is not None
    assert Path(response.csv_path).exists()
    assert Path(response.json_path).exists()

    # Check metrics
    metrics = response.summary_metrics
    assert metrics.total_establishments == 100
    assert metrics.average_worker_count > 20
    assert metrics.average_risk_score > 0
    assert len(metrics.sector_distribution) >= 5
    assert len(metrics.risk_distribution) == 3


def test_synthetic_record_attributes():
    records = SyntheticDatasetGenerator.get_or_generate_dataset()
    assert len(records) >= 100

    r = records[0]
    assert r.establishment_id.startswith("EST-")
    assert len(r.name) > 3
    assert r.state in ["Maharashtra", "Tamil Nadu", "Gujarat", "Haryana", "Karnataka", "Uttar Pradesh"]
    assert 10 <= r.worker_count <= 4000
    assert 0.05 <= r.contract_worker_ratio <= 0.90
    assert 0.0 <= r.female_worker_ratio <= 1.0
    assert 10.0 <= r.ground_truth_risk_score <= 100.0
    assert r.ground_truth_inspection_priority in ["HIGH", "MEDIUM", "LOW"]


def test_dataset_api_endpoints(client):
    # GET summary
    sum_resp = client.get("/api/v1/dataset/summary")
    assert sum_resp.status_code == 200
    sum_data = sum_resp.json()
    assert sum_data["total_establishments"] >= 100
    assert len(sum_data["sector_distribution"]) >= 1

    # GET sample
    sample_resp = client.get("/api/v1/dataset/sample?limit=5")
    assert sample_resp.status_code == 200
    sample_data = sample_resp.json()
    assert len(sample_data) == 5

    # POST generate
    gen_resp = client.post("/api/v1/dataset/generate", json={"num_samples": 50, "seed": 999, "save_to_disk": False})
    assert gen_resp.status_code == 200
    assert gen_resp.json()["samples_generated"] == 50
