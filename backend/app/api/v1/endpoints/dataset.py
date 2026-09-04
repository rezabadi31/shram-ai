from typing import Optional, List
from fastapi import APIRouter, Query, Body
from app.schemas.dataset import (
    DatasetGenerationConfig,
    DatasetGenerationResponse,
    DatasetSummaryMetrics,
    EstablishmentRecordSynthetic,
)
from app.dataset.generator import SyntheticDatasetGenerator

router = APIRouter()


@router.post("/generate", response_model=DatasetGenerationResponse, tags=["Synthetic Dataset Generator"])
async def generate_synthetic_dataset(config: Optional[DatasetGenerationConfig] = Body(default=None)):
    """
    Generates a statistically realistic dataset of Indian industrial establishments (default: 1,000 records).
    Saves to data/synthetic_establishments.csv and data/synthetic_establishments.json for ML training.
    """
    cfg = config or DatasetGenerationConfig()
    return SyntheticDatasetGenerator.generate_dataset(
        num_samples=cfg.num_samples,
        seed=cfg.seed or 42,
        save_to_disk=cfg.save_to_disk,
    )


@router.get("/summary", response_model=DatasetSummaryMetrics, tags=["Synthetic Dataset Generator"])
async def get_dataset_summary():
    """
    Returns distribution metrics across sectors, risk levels, and simulated statutory violations.
    """
    records = SyntheticDatasetGenerator.get_or_generate_dataset()
    return SyntheticDatasetGenerator.compute_summary_metrics(records)


@router.get("/sample", response_model=List[EstablishmentRecordSynthetic], tags=["Synthetic Dataset Generator"])
async def get_dataset_sample(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    priority: Optional[str] = Query(None, description="Filter by HIGH, MEDIUM, LOW"),
):
    """
    Returns paginated sample synthetic establishment records for UI data exploration.
    """
    records = SyntheticDatasetGenerator.get_or_generate_dataset()
    if priority:
        records = [r for r in records if r.ground_truth_inspection_priority == priority.upper()]
    return records[offset : offset + limit]
