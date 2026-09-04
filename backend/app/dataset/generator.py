import os
import csv
import json
import random
from typing import List, Dict, Any, Tuple
from pathlib import Path

from app.schemas.dataset import (
    EstablishmentRecordSynthetic,
    DatasetSummaryMetrics,
    SectorDistributionItem,
    RiskDistributionItem,
    DatasetGenerationResponse,
)


class SyntheticDatasetGenerator:
    INDIAN_LOCATIONS = [
        ("Maharashtra", "Pune", "Auto & Engineering Hub"),
        ("Maharashtra", "Thane", "Chemical & Industrial Belt"),
        ("Tamil Nadu", "Coimbatore", "Textile & Pump Manufacturing"),
        ("Tamil Nadu", "Sriperumbudur", "Electronics & Automotive"),
        ("Gujarat", "Surat", "Textiles & Diamond Processing"),
        ("Gujarat", "Vadodara", "Petrochemicals & Heavy Engineering"),
        ("Haryana", "Gurugram", "Auto Components & Logistics"),
        ("Haryana", "Panipat", "Textile & Handloom"),
        ("Karnataka", "Bengaluru Urban", "Electronics & Precision Engineering"),
        ("Karnataka", "Peenya", "Small Scale Industrial Cluster"),
        ("Uttar Pradesh", "Noida", "Consumer Goods & Logistics"),
        ("Uttar Pradesh", "Kanpur", "Leather & Heavy Chemical"),
    ]

    SECTORS = [
        {"name": "Automobile & Auto Components", "hazard_prob": 0.25, "contract_bias": 0.35, "base_risk": 35},
        {"name": "Textile, Garments & Apparel", "hazard_prob": 0.15, "contract_bias": 0.45, "base_risk": 45},
        {"name": "Chemical & Hazardous Processing", "hazard_prob": 0.85, "contract_bias": 0.30, "base_risk": 60},
        {"name": "Construction & Infrastructure", "hazard_prob": 0.70, "contract_bias": 0.65, "base_risk": 65},
        {"name": "Food Processing & Agro Industries", "hazard_prob": 0.20, "contract_bias": 0.30, "base_risk": 30},
        {"name": "Warehousing & Supply Chain Logistics", "hazard_prob": 0.30, "contract_bias": 0.50, "base_risk": 40},
        {"name": "Electronics & Precision Fabrication", "hazard_prob": 0.20, "contract_bias": 0.25, "base_risk": 25},
    ]

    NAME_PREFIXES = [
        "Bharat", "Apex", "Shree", "Hindustan", "Surya", "Zenith", "Tata", "Vanguard", 
        "Swastik", "Navkar", "Pinnacle", "Sterling", "Kalyan", "Shakti", "Premier", "Delta"
    ]
    NAME_SUFFIXES = [
        "Industries Ltd.", "Enterprises Pvt Ltd", "Manufacturing Corp", "Engineering Works",
        "Fabrics & Garments", "Synthetics Ltd", "Components India", "Processing Co."
    ]

    _cached_dataset: List[EstablishmentRecordSynthetic] = []

    @classmethod
    def generate_dataset(
        cls,
        num_samples: int = 1000,
        seed: int = 42,
        save_to_disk: bool = True,
    ) -> DatasetGenerationResponse:
        """
        Generates N statistically realistic establishment compliance records
        calibrated to Indian labour inspection realities.
        """
        random.seed(seed)
        records: List[EstablishmentRecordSynthetic] = []

        for i in range(1, num_samples + 1):
            est_id = f"EST-{i:04d}"
            state, district, _ = random.choice(cls.INDIAN_LOCATIONS)
            sector_obj = random.choice(cls.SECTORS)
            sector_name = sector_obj["name"]

            prefix = random.choice(cls.NAME_PREFIXES)
            suffix = random.choice(cls.NAME_SUFFIXES)
            name = f"{prefix} {suffix}"

            # Log-normal workforce size distribution: median ~85, tail up to 2500
            worker_count = int(random.lognormvariate(4.4, 0.85))
            worker_count = max(12, min(worker_count, 3500))

            # Hazardous process likelihood
            is_hazardous = random.random() < sector_obj["hazard_prob"]

            # Contract worker ratio (beta distribution)
            contract_ratio = round(random.betavariate(2.0, 5.0) + sector_obj["contract_bias"] * 0.4, 3)
            contract_ratio = min(max(0.05, contract_ratio), 0.90)

            # Female worker ratio
            if "Textile" in sector_name or "Electronics" in sector_name:
                female_ratio = round(random.uniform(0.40, 0.75), 3)
            else:
                female_ratio = round(random.uniform(0.05, 0.35), 3)

            # Violation probabilities scaled by sector and contract ratio
            prob_factor = 0.8 + (contract_ratio * 0.8) + (0.4 if is_hazardous else 0.0)

            wage_violations = int(random.expovariate(0.9) * prob_factor) if random.random() < 0.35 * prob_factor else 0
            ot_violations = int(random.expovariate(1.0) * prob_factor) if random.random() < 0.40 * prob_factor else 0
            deduction_violations = int(random.expovariate(1.2) * prob_factor) if random.random() < 0.25 * prob_factor else 0
            missing_registers = int(random.expovariate(1.5)) if random.random() < 0.30 else 0

            # Cross-document anomalies
            ghost_workers = int(random.expovariate(1.5)) if (contract_ratio > 0.4 and random.random() < 0.20) else 0
            uncompensated_workers = int(random.expovariate(1.8)) if random.random() < 0.15 else 0
            disbursement_mismatches = int(random.expovariate(1.2)) if (wage_violations > 0 and random.random() < 0.30) else 0

            # Historical non-compliances & grievances
            inspection_history = int(random.expovariate(1.2)) if random.random() < 0.45 else 0
            grievance_count = int(random.expovariate(1.5)) if (wage_violations + ot_violations > 2) else 0

            # Ground-truth mathematical calibrated risk score (0 - 100)
            base_score = sector_obj["base_risk"]
            violation_penalty = (wage_violations * 8.5) + (ot_violations * 6.0) + (deduction_violations * 5.0) + (missing_registers * 4.0)
            anomaly_penalty = (ghost_workers * 12.0) + (uncompensated_workers * 10.0) + (disbursement_mismatches * 8.0)
            size_penalty = 5.0 if worker_count >= 250 else 0.0
            history_penalty = (inspection_history * 4.0) + (grievance_count * 5.0)

            raw_risk = base_score + violation_penalty + anomaly_penalty + size_penalty + history_penalty
            raw_risk += random.uniform(-4.0, 4.0)
            risk_score = round(min(max(10.0, raw_risk), 98.5), 1)

            if risk_score >= 70.0:
                priority = "HIGH"
            elif risk_score >= 45.0:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            record = EstablishmentRecordSynthetic(
                establishment_id=est_id,
                name=name,
                state=state,
                district=district,
                industry_sector=sector_name,
                hazardous_process=is_hazardous,
                worker_count=worker_count,
                contract_worker_ratio=contract_ratio,
                female_worker_ratio=female_ratio,
                wage_violation_count=wage_violations,
                ot_violation_count=ot_violations,
                deduction_violation_count=deduction_violations,
                missing_register_count=missing_registers,
                ghost_worker_count=ghost_workers,
                uncompensated_worker_count=uncompensated_workers,
                disbursement_mismatch_count=disbursement_mismatches,
                inspection_history_violations=inspection_history,
                grievance_complaint_count=grievance_count,
                ground_truth_risk_score=risk_score,
                ground_truth_inspection_priority=priority,
            )
            records.append(record)

        if save_to_disk or len(records) >= len(cls._cached_dataset):
            cls._cached_dataset = records
        metrics = cls.compute_summary_metrics(records)

        csv_path = None
        json_path = None

        if save_to_disk:
            data_dir = Path("data")
            data_dir.mkdir(parents=True, exist_ok=True)
            csv_path = str(data_dir / "synthetic_establishments.csv")
            json_path = str(data_dir / "synthetic_establishments.json")

            # Write CSV
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(records[0].model_dump().keys()))
                writer.writeheader()
                for r in records:
                    writer.writerow(r.model_dump())

            # Write JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in records], f, indent=2)

        return DatasetGenerationResponse(
            status="SUCCESS",
            samples_generated=len(records),
            csv_path=csv_path,
            json_path=json_path,
            summary_metrics=metrics,
        )

    @classmethod
    def compute_summary_metrics(cls, records: List[EstablishmentRecordSynthetic]) -> DatasetSummaryMetrics:
        """Computes statistical breakdown across sectors and risk priority."""
        total = len(records)
        if total == 0:
            return DatasetSummaryMetrics(
                total_establishments=0,
                average_worker_count=0.0,
                average_risk_score=0.0,
                sector_distribution=[],
                risk_distribution=[],
                total_violations_simulated=0,
                total_ghost_workers_simulated=0,
            )

        avg_workers = sum(r.worker_count for r in records) / total
        avg_risk = sum(r.ground_truth_risk_score for r in records) / total

        # Sector distribution
        sector_counts: Dict[str, int] = {}
        for r in records:
            sector_counts[r.industry_sector] = sector_counts.get(r.industry_sector, 0) + 1

        sector_items = [
            SectorDistributionItem(
                sector=sec,
                count=count,
                percentage=round((count / total) * 100.0, 1),
            )
            for sec, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        # Risk distribution
        risk_counts: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in records:
            risk_counts[r.ground_truth_inspection_priority] = risk_counts.get(r.ground_truth_inspection_priority, 0) + 1

        risk_items = [
            RiskDistributionItem(
                priority=p,
                count=count,
                percentage=round((count / total) * 100.0, 1),
            )
            for p, count in risk_counts.items()
        ]

        total_violations = sum(
            r.wage_violation_count + r.ot_violation_count + r.deduction_violation_count + r.missing_register_count
            for r in records
        )
        total_ghosts = sum(r.ghost_worker_count for r in records)

        return DatasetSummaryMetrics(
            total_establishments=total,
            average_worker_count=round(avg_workers, 1),
            average_risk_score=round(avg_risk, 1),
            sector_distribution=sector_items,
            risk_distribution=risk_items,
            total_violations_simulated=total_violations,
            total_ghost_workers_simulated=total_ghosts,
        )

    @classmethod
    def get_or_generate_dataset(cls) -> List[EstablishmentRecordSynthetic]:
        """Loads cached dataset or generates 1,000 records if not yet created."""
        if cls._cached_dataset and len(cls._cached_dataset) >= 500:
            return cls._cached_dataset

        json_path = Path("data/synthetic_establishments.json")
        if json_path.exists():
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cls._cached_dataset = [EstablishmentRecordSynthetic(**item) for item in data]
                    return cls._cached_dataset
            except Exception:
                pass

        # Generate fresh
        res = cls.generate_dataset(num_samples=1000, seed=42, save_to_disk=True)
        return cls._cached_dataset
