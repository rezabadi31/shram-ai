from typing import List
from fastapi import APIRouter
from app.schemas.analytics import (
    MacroOverviewResponse,
    JurisdictionMetric,
    SectorRiskMetric,
)
from app.analytics.service import AnalyticsService

router = APIRouter()


@router.get("/macro-overview", response_model=MacroOverviewResponse)
def get_macro_overview():
    """
    Retrieve national and regional macro compliance overview, including
    jurisdiction aggregations, sector hazard breakdown, and compliance trends.
    """
    return AnalyticsService.get_macro_overview()


@router.get("/jurisdictions", response_model=List[JurisdictionMetric])
def list_jurisdictions():
    """
    List multi-district compliance metrics across Central and State Spheres.
    """
    return AnalyticsService.get_jurisdictions()


@router.get("/sector-risk-matrix", response_model=List[SectorRiskMetric])
def get_sector_risk_matrix():
    """
    Retrieve hazard tier mapping and non-compliance risk rates across industry sectors.
    """
    return AnalyticsService.get_sectors()
