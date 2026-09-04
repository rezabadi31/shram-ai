from typing import List
from app.schemas.analytics import (
    JurisdictionMetric,
    SectorRiskMetric,
    MonthlyTrendPoint,
    MacroOverviewResponse,
)


class AnalyticsService:
    @staticmethod
    def get_jurisdictions() -> List[JurisdictionMetric]:
        return [
            JurisdictionMetric(
                jurisdiction_id="JUR-PUN-01",
                jurisdiction_name="Central Sphere — Pune Cluster",
                sphere="CENTRAL",
                total_establishments=1840,
                audited_count=1420,
                high_risk_count=168,
                average_risk_score=52.4,
                compliance_rate_pct=81.2,
                arrears_recovered_inr=4250000.0,
                notices_issued_count=94,
            ),
            JurisdictionMetric(
                jurisdiction_id="JUR-MUM-02",
                jurisdiction_name="Central Sphere — Mumbai Port & Suburban",
                sphere="CENTRAL",
                total_establishments=2450,
                audited_count=1980,
                high_risk_count=242,
                average_risk_score=58.1,
                compliance_rate_pct=76.8,
                arrears_recovered_inr=6820000.0,
                notices_issued_count=142,
            ),
            JurisdictionMetric(
                jurisdiction_id="JUR-THA-03",
                jurisdiction_name="Thane — Belapur Chemical Industrial Belt",
                sphere="CENTRAL",
                total_establishments=1620,
                audited_count=1290,
                high_risk_count=215,
                average_risk_score=64.8,
                compliance_rate_pct=71.4,
                arrears_recovered_inr=3910000.0,
                notices_issued_count=118,
            ),
            JurisdictionMetric(
                jurisdiction_id="JUR-NAG-04",
                jurisdiction_name="Vidarbha & Nagpur Mining-Logistics Hub",
                sphere="CENTRAL",
                total_establishments=1180,
                audited_count=940,
                high_risk_count=138,
                average_risk_score=54.6,
                compliance_rate_pct=79.5,
                arrears_recovered_inr=2140000.0,
                notices_issued_count=62,
            ),
            JurisdictionMetric(
                jurisdiction_id="JUR-AHM-05",
                jurisdiction_name="Ahmedabad — Sanand Manufacturing Corridor",
                sphere="CENTRAL",
                total_establishments=1360,
                audited_count=1120,
                high_risk_count=154,
                average_risk_score=53.2,
                compliance_rate_pct=80.1,
                arrears_recovered_inr=2880000.0,
                notices_issued_count=79,
            ),
        ]

    @staticmethod
    def get_sectors() -> List[SectorRiskMetric]:
        return [
            SectorRiskMetric(
                sector_id="SEC-CHEM",
                sector_name="Chemicals, Petrochem & Active Pharma",
                hazard_tier="HIGH_HAZARD",
                total_units=1240,
                non_compliance_rate_pct=28.4,
                top_violation_code="OSHWC Code Sec 96 (Safety Committee & PPE)",
                estimated_underpayment_inr=5400000.0,
            ),
            SectorRiskMetric(
                sector_id="SEC-ENG",
                sector_name="Heavy Machinery & Metal Fabrication",
                hazard_tier="HIGH_HAZARD",
                total_units=1890,
                non_compliance_rate_pct=22.6,
                top_violation_code="Code on Wages Sec 54(1) (Shift B Differential)",
                estimated_underpayment_inr=4200000.0,
            ),
            SectorRiskMetric(
                sector_id="SEC-LOG",
                sector_name="E-Commerce Fulfillment & Warehousing",
                hazard_tier="MEDIUM_HAZARD",
                total_units=2150,
                non_compliance_rate_pct=18.2,
                top_violation_code="Code on Wages Sec 50 (Muster Roll Discrepancies)",
                estimated_underpayment_inr=3100000.0,
            ),
            SectorRiskMetric(
                sector_id="SEC-TEX",
                sector_name="Garment Manufacturing & Spinning Mills",
                hazard_tier="MEDIUM_HAZARD",
                total_units=1680,
                non_compliance_rate_pct=19.5,
                top_violation_code="Code on Wages Sec 13 (Double-Rate Overtime)",
                estimated_underpayment_inr=3900000.0,
            ),
            SectorRiskMetric(
                sector_id="SEC-IT",
                sector_name="Technology Services & ITES Operations",
                hazard_tier="LOW_HAZARD",
                total_units=1490,
                non_compliance_rate_pct=6.8,
                top_violation_code="OSHWC Code Sec 24 (Working Hours & Night Shifts)",
                estimated_underpayment_inr=1600000.0,
            ),
        ]

    @staticmethod
    def get_monthly_trend() -> List[MonthlyTrendPoint]:
        return [
            MonthlyTrendPoint(month="Jan 2024", audits_completed=480, violations_detected=162, safe_harbour_achieved=32, compliance_index=72.1),
            MonthlyTrendPoint(month="Feb 2024", audits_completed=540, violations_detected=174, safe_harbour_achieved=45, compliance_index=73.5),
            MonthlyTrendPoint(month="Mar 2024", audits_completed=620, violations_detected=188, safe_harbour_achieved=58, compliance_index=74.8),
            MonthlyTrendPoint(month="Apr 2024", audits_completed=590, violations_detected=154, safe_harbour_achieved=64, compliance_index=76.2),
            MonthlyTrendPoint(month="May 2024", audits_completed=680, violations_detected=148, safe_harbour_achieved=79, compliance_index=77.9),
            MonthlyTrendPoint(month="Jun 2024", audits_completed=730, violations_detected=139, safe_harbour_achieved=92, compliance_index=79.4),
            MonthlyTrendPoint(month="Jul 2024", audits_completed=810, violations_detected=126, safe_harbour_achieved=112, compliance_index=81.2),
            MonthlyTrendPoint(month="Aug 2024", audits_completed=890, violations_detected=118, safe_harbour_achieved=134, compliance_index=82.8),
        ]

    @classmethod
    def get_macro_overview(cls) -> MacroOverviewResponse:
        jurisdictions = cls.get_jurisdictions()
        sectors = cls.get_sectors()
        trend = cls.get_monthly_trend()

        total_establishments = sum(j.total_establishments for j in jurisdictions)
        total_arrears = sum(j.arrears_recovered_inr for j in jurisdictions)
        total_notices = sum(j.notices_issued_count for j in jurisdictions)

        return MacroOverviewResponse(
            national_compliance_index=78.4,
            total_registered_workforce=1425000,
            total_active_establishments=total_establishments,
            total_inspections_scheduled_quarter=640,
            total_penalties_assessed_inr=48500000.0,
            total_arrears_recovered_inr=total_arrears,
            safe_harbour_achieved_count=184,
            jurisdictions=jurisdictions,
            sectors=sectors,
            monthly_trend=trend,
            metadata={
                "reporting_authority": "Office of the Chief Labour Commissioner (Central)",
                "data_pipeline": "ShramAI Macro Intelligence Service",
                "coverage_spheres": ["CENTRAL_SPHERE", "MAJOR_INDUSTRIAL_CORRIDORS"],
            },
        )
