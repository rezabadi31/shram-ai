import math
from typing import List, Dict, Any, Tuple, Optional
from app.schemas.features import (
    FeatureCategory,
    FeatureDefinition,
    FeatureVectorItem,
    FeatureExtractionResponse,
    FeatureSummaryStats,
    DatasetFeatureMatrixSummary,
)
from app.dataset.generator import SyntheticDatasetGenerator


class RiskFeatureExtractor:
    SECTOR_PRIORS = {
        "Automobile & Auto Components": 0.45,
        "Textile, Garments & Apparel": 0.55,
        "Chemical & Hazardous Processing": 0.85,
        "Construction & Infrastructure": 0.80,
        "Food Processing & Agro Industries": 0.35,
        "Warehousing & Supply Chain Logistics": 0.50,
        "Electronics & Precision Fabrication": 0.30,
    }

    DEFINITIONS: List[FeatureDefinition] = [
        # 1. Demographic & Structural (5)
        FeatureDefinition(
            name="feat_log_workforce",
            label="Log Workforce Scale",
            category=FeatureCategory.DEMOGRAPHIC,
            description="Log-transformed workforce scale ln(worker_count + 1)",
            formula="ln(workers + 1)",
            weight_hint=0.08,
        ),
        FeatureDefinition(
            name="feat_contract_ratio",
            label="Contract Labour Ratio",
            category=FeatureCategory.DEMOGRAPHIC,
            description="Proportion of contractual and third-party outsourced labour",
            formula="contract_workers / total_workers",
            weight_hint=0.12,
        ),
        FeatureDefinition(
            name="feat_female_ratio",
            label="Female Workforce Participation",
            category=FeatureCategory.DEMOGRAPHIC,
            description="Proportion of female employees requiring mandatory maternity/creche provisions",
            formula="female_workers / total_workers",
            weight_hint=0.04,
        ),
        FeatureDefinition(
            name="feat_hazardous_process",
            label="Hazardous Process Indicator",
            category=FeatureCategory.DEMOGRAPHIC,
            description="Binary flag for Schedule I hazardous industries under OSHWC Code",
            formula="1 if hazardous else 0",
            weight_hint=0.10,
        ),
        FeatureDefinition(
            name="feat_sector_risk_weight",
            label="Sector Domain Risk Weight",
            category=FeatureCategory.DEMOGRAPHIC,
            description="Actuarial baseline risk factor calibrated for the industrial sector",
            formula="sector_prior_weight",
            weight_hint=0.09,
        ),

        # 2. Deterministic Violation Density (4)
        FeatureDefinition(
            name="feat_wage_violation_rate",
            label="Minimum Wage Violation Density",
            category=FeatureCategory.DETERMINISTIC,
            description="Rate of workers paid below statutory national floor wage",
            formula="wage_violations / max(1, workers * 0.1)",
            weight_hint=0.15,
        ),
        FeatureDefinition(
            name="feat_ot_violation_rate",
            label="Overtime Rate Violation Density",
            category=FeatureCategory.DETERMINISTIC,
            description="Rate of hours compensated below double normal rate under Code on Wages Sec. 14",
            formula="ot_violations / max(1, workers * 0.1)",
            weight_hint=0.12,
        ),
        FeatureDefinition(
            name="feat_deduction_breach_rate",
            label="Deduction Cap Breach Density",
            category=FeatureCategory.DETERMINISTIC,
            description="Frequency of wage deductions exceeding 50% statutory threshold",
            formula="deduction_violations / max(1, workers * 0.1)",
            weight_hint=0.10,
        ),
        FeatureDefinition(
            name="feat_missing_register_ratio",
            label="Statutory Register Default Ratio",
            category=FeatureCategory.DETERMINISTIC,
            description="Proportion of 7 mandatory registers missing from audited filings",
            formula="missing_registers / 7.0",
            weight_hint=0.14,
        ),

        # 3. Cross-Document Anomaly Signals (4)
        FeatureDefinition(
            name="feat_ghost_worker_ratio",
            label="Ghost Worker Anomaly Density",
            category=FeatureCategory.ANOMALY,
            description="Ratio of workers receiving net wage disbursement with zero muster attendance",
            formula="ghost_workers / max(1, workers * 0.05)",
            weight_hint=0.16,
        ),
        FeatureDefinition(
            name="feat_uncompensated_ratio",
            label="Uncompensated Attendance Ratio",
            category=FeatureCategory.ANOMALY,
            description="Ratio of workers present on muster roll but receiving zero wage payout",
            formula="uncompensated / max(1, workers * 0.05)",
            weight_hint=0.14,
        ),
        FeatureDefinition(
            name="feat_disbursement_mismatch_score",
            label="Bank UTR Net Diversion Score",
            category=FeatureCategory.ANOMALY,
            description="Discrepancy score between Form B net wages and bank payment transfer sums",
            formula="disbursement_mismatches * 0.25",
            weight_hint=0.15,
        ),
        FeatureDefinition(
            name="feat_contractor_suppression_score",
            label="Contractor Headcount Suppression",
            category=FeatureCategory.ANOMALY,
            description="Indicator of factory turnstile access surpassing declared Form A headcount",
            formula="1 if turnstile > declared else 0",
            weight_hint=0.11,
        ),

        # 4. Historical & Enforcement Signals (3)
        FeatureDefinition(
            name="feat_prior_inspection_violations",
            label="Historical Inspection Defaults",
            category=FeatureCategory.HISTORICAL,
            description="Statutory violation notices issued during preceding 24 months",
            formula="min(1.0, past_violations / 5.0)",
            weight_hint=0.08,
        ),
        FeatureDefinition(
            name="feat_worker_grievance_rate",
            label="Worker Grievance Escalations",
            category=FeatureCategory.HISTORICAL,
            description="Number of labour officer grievances lodged per establishment",
            formula="min(1.0, grievances / 3.0)",
            weight_hint=0.07,
        ),
        FeatureDefinition(
            name="feat_inspection_recency_penalty",
            label="Inspection Recency Latency",
            category=FeatureCategory.HISTORICAL,
            description="Actuarial decay factor penalizing prolonged absence of physical inspection",
            formula="time_since_inspection_decay",
            weight_hint=0.06,
        ),

        # 5. High-Risk Interaction Features (6)
        FeatureDefinition(
            name="feat_contract_x_hazardous",
            label="Contract Labour in Hazardous Operations",
            category=FeatureCategory.INTERACTION,
            description="Interaction multiplier of high contract labour in hazardous industrial plants",
            formula="contract_ratio * hazardous_flag",
            weight_hint=0.16,
        ),
        FeatureDefinition(
            name="feat_workforce_x_missing_registers",
            label="Large Workforce Statutory Opacity",
            category=FeatureCategory.INTERACTION,
            description="High risk interaction when a large workforce operates without mandatory registers",
            formula="(workers / 500) * missing_register_ratio",
            weight_hint=0.14,
        ),
        FeatureDefinition(
            name="feat_wage_x_disbursement_discrepancy",
            label="Wage Breach & Bank Skimming Co-occurrence",
            category=FeatureCategory.INTERACTION,
            description="Co-occurrence of minimum wage underpayment with bank disbursement diversions",
            formula="wage_rate * disbursement_score",
            weight_hint=0.15,
        ),
        FeatureDefinition(
            name="feat_ghost_x_contract_ratio",
            label="Ghost Payroll & Contractor Dependency",
            category=FeatureCategory.INTERACTION,
            description="Compound risk of phantom headcount coupled with outsourced contractor reliance",
            formula="ghost_ratio * contract_ratio",
            weight_hint=0.15,
        ),
        FeatureDefinition(
            name="feat_composite_violation_index",
            label="Composite Deterministic Violation Index",
            category=FeatureCategory.INTERACTION,
            description="Harmonized weighted index across all 4 primary statutory violation rates",
            formula="0.35*wage + 0.25*ot + 0.20*ded + 0.20*reg",
            weight_hint=0.18,
        ),
        FeatureDefinition(
            name="feat_composite_anomaly_index",
            label="Composite Cross-Register Anomaly Index",
            category=FeatureCategory.INTERACTION,
            description="Harmonized weighted index across all 4 cross-document anomaly signals",
            formula="0.35*ghost + 0.30*uncomp + 0.20*skim + 0.15*supp",
            weight_hint=0.18,
        ),
    ]

    @classmethod
    def get_feature_definitions(cls) -> List[FeatureDefinition]:
        return cls.DEFINITIONS

    @classmethod
    def extract_features(
        cls,
        establishment_id: str = "EST-001",
        worker_count: int = 420,
        contract_worker_ratio: float = 0.42,
        female_worker_ratio: float = 0.28,
        hazardous_process: bool = True,
        industry_sector: str = "Automobile & Auto Components",
        wage_violation_count: int = 3,
        ot_violation_count: int = 2,
        deduction_violation_count: int = 1,
        missing_register_count: int = 2,
        ghost_worker_count: int = 1,
        uncompensated_worker_count: int = 1,
        disbursement_mismatch_count: int = 1,
        inspection_history_violations: int = 2,
        grievance_complaint_count: int = 1,
    ) -> FeatureExtractionResponse:
        """
        Extracts the exact 22-dimensional feature vector with normalized values.
        """
        # Demographic
        feat_log_workforce = round(math.log(max(1, worker_count) + 1), 4)
        feat_contract_ratio = round(min(max(0.0, contract_worker_ratio), 1.0), 4)
        feat_female_ratio = round(min(max(0.0, female_worker_ratio), 1.0), 4)
        feat_hazardous_process = 1.0 if hazardous_process else 0.0
        feat_sector_risk_weight = cls.SECTOR_PRIORS.get(industry_sector, 0.45)

        # Deterministic
        scale_div = max(1.0, worker_count * 0.1)
        feat_wage_violation_rate = round(min(1.0, wage_violation_count / scale_div), 4)
        feat_ot_violation_rate = round(min(1.0, ot_violation_count / scale_div), 4)
        feat_deduction_breach_rate = round(min(1.0, deduction_violation_count / scale_div), 4)
        feat_missing_register_ratio = round(min(1.0, missing_register_count / 7.0), 4)

        # Anomalies
        anom_div = max(1.0, worker_count * 0.05)
        feat_ghost_worker_ratio = round(min(1.0, ghost_worker_count / anom_div), 4)
        feat_uncompensated_ratio = round(min(1.0, uncompensated_worker_count / anom_div), 4)
        feat_disbursement_mismatch_score = round(min(1.0, disbursement_mismatch_count * 0.25), 4)
        feat_contractor_suppression_score = 1.0 if (contract_worker_ratio > 0.4 and worker_count > 100) else 0.0

        # Historical
        feat_prior_inspection_violations = round(min(1.0, inspection_history_violations / 5.0), 4)
        feat_worker_grievance_rate = round(min(1.0, grievance_complaint_count / 3.0), 4)
        feat_inspection_recency_penalty = 0.65

        # Interactions
        feat_contract_x_hazardous = round(feat_contract_ratio * feat_hazardous_process, 4)
        feat_workforce_x_missing_registers = round(min(1.0, (worker_count / 500.0) * feat_missing_register_ratio), 4)
        feat_wage_x_disbursement_discrepancy = round(feat_wage_violation_rate * feat_disbursement_mismatch_score, 4)
        feat_ghost_x_contract_ratio = round(feat_ghost_worker_ratio * feat_contract_ratio, 4)
        feat_composite_violation_index = round(
            (0.35 * feat_wage_violation_rate)
            + (0.25 * feat_ot_violation_rate)
            + (0.20 * feat_deduction_breach_rate)
            + (0.20 * feat_missing_register_ratio),
            4,
        )
        feat_composite_anomaly_index = round(
            (0.35 * feat_ghost_worker_ratio)
            + (0.30 * feat_uncompensated_ratio)
            + (0.20 * feat_disbursement_mismatch_score)
            + (0.15 * feat_contractor_suppression_score),
            4,
        )

        values_dict = {
            "feat_log_workforce": (feat_log_workforce, feat_log_workforce / 8.0),
            "feat_contract_ratio": (feat_contract_ratio, feat_contract_ratio),
            "feat_female_ratio": (feat_female_ratio, feat_female_ratio),
            "feat_hazardous_process": (feat_hazardous_process, feat_hazardous_process),
            "feat_sector_risk_weight": (feat_sector_risk_weight, feat_sector_risk_weight),
            "feat_wage_violation_rate": (feat_wage_violation_rate, feat_wage_violation_rate),
            "feat_ot_violation_rate": (feat_ot_violation_rate, feat_ot_violation_rate),
            "feat_deduction_breach_rate": (feat_deduction_breach_rate, feat_deduction_breach_rate),
            "feat_missing_register_ratio": (feat_missing_register_ratio, feat_missing_register_ratio),
            "feat_ghost_worker_ratio": (feat_ghost_worker_ratio, feat_ghost_worker_ratio),
            "feat_uncompensated_ratio": (feat_uncompensated_ratio, feat_uncompensated_ratio),
            "feat_disbursement_mismatch_score": (feat_disbursement_mismatch_score, feat_disbursement_mismatch_score),
            "feat_contractor_suppression_score": (feat_contractor_suppression_score, feat_contractor_suppression_score),
            "feat_prior_inspection_violations": (feat_prior_inspection_violations, feat_prior_inspection_violations),
            "feat_worker_grievance_rate": (feat_worker_grievance_rate, feat_worker_grievance_rate),
            "feat_inspection_recency_penalty": (feat_inspection_recency_penalty, feat_inspection_recency_penalty),
            "feat_contract_x_hazardous": (feat_contract_x_hazardous, feat_contract_x_hazardous),
            "feat_workforce_x_missing_registers": (feat_workforce_x_missing_registers, feat_workforce_x_missing_registers),
            "feat_wage_x_disbursement_discrepancy": (feat_wage_x_disbursement_discrepancy, feat_wage_x_disbursement_discrepancy),
            "feat_ghost_x_contract_ratio": (feat_ghost_x_contract_ratio, feat_ghost_x_contract_ratio),
            "feat_composite_violation_index": (feat_composite_violation_index, feat_composite_violation_index),
            "feat_composite_anomaly_index": (feat_composite_anomaly_index, feat_composite_anomaly_index),
        }

        vector_items: List[FeatureVectorItem] = []
        raw_vector: Dict[str, float] = {}

        for defn in cls.DEFINITIONS:
            raw_val, norm_val = values_dict[defn.name]
            norm_val = round(min(max(0.0, norm_val), 1.0), 4)
            vector_items.append(
                FeatureVectorItem(
                    name=defn.name,
                    label=defn.label,
                    category=defn.category,
                    raw_value=raw_val,
                    normalized_value=norm_val,
                    formula=defn.formula,
                )
            )
            raw_vector[defn.name] = raw_val

        return FeatureExtractionResponse(
            establishment_id=establishment_id,
            feature_count=len(vector_items),
            features=vector_items,
            vector=raw_vector,
        )

    @classmethod
    def extract_matrix_from_dataset(cls) -> Tuple[List[List[float]], List[float], List[str]]:
        """
        Extracts (X, y, feature_names) from the synthetic establishment dataset.
        """
        records = SyntheticDatasetGenerator.get_or_generate_dataset()
        feature_names = [d.name for d in cls.DEFINITIONS]

        X: List[List[float]] = []
        y: List[float] = []

        for r in records:
            res = cls.extract_features(
                establishment_id=r.establishment_id,
                worker_count=r.worker_count,
                contract_worker_ratio=r.contract_worker_ratio,
                female_worker_ratio=r.female_worker_ratio,
                hazardous_process=r.hazardous_process,
                industry_sector=r.industry_sector,
                wage_violation_count=r.wage_violation_count,
                ot_violation_count=r.ot_violation_count,
                deduction_violation_count=r.deduction_violation_count,
                missing_register_count=r.missing_register_count,
                ghost_worker_count=r.ghost_worker_count,
                uncompensated_worker_count=r.uncompensated_worker_count,
                disbursement_mismatch_count=r.disbursement_mismatch_count,
                inspection_history_violations=r.inspection_history_violations,
                grievance_complaint_count=r.grievance_complaint_count,
            )
            row = [res.vector[f_name] for f_name in feature_names]
            X.append(row)
            y.append(r.ground_truth_risk_score)

        return X, y, feature_names

    @classmethod
    def compute_matrix_summary(cls) -> DatasetFeatureMatrixSummary:
        """
        Computes summary statistics (mean, std, min, max) for each of the 22 features across the dataset.
        """
        X, _, feature_names = cls.extract_matrix_from_dataset()
        n_samples = len(X)
        if n_samples == 0:
            return DatasetFeatureMatrixSummary(sample_count=0, feature_count=22, features=[])

        summary_list: List[FeatureSummaryStats] = []
        defn_map = {d.name: d for d in cls.DEFINITIONS}

        for col_idx, f_name in enumerate(feature_names):
            vals = [row[col_idx] for row in X]
            mean_val = sum(vals) / n_samples
            var_val = sum((v - mean_val) ** 2 for v in vals) / n_samples
            std_val = math.sqrt(var_val)
            min_val = min(vals)
            max_val = max(vals)
            defn = defn_map[f_name]

            summary_list.append(
                FeatureSummaryStats(
                    name=f_name,
                    label=defn.label,
                    category=defn.category,
                    mean=round(mean_val, 4),
                    std=round(std_val, 4),
                    min_val=round(min_val, 4),
                    max_val=round(max_val, 4),
                )
            )

        return DatasetFeatureMatrixSummary(
            sample_count=n_samples,
            feature_count=len(feature_names),
            features=summary_list,
        )
