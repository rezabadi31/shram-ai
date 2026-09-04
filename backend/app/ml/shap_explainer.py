import math
from typing import List, Dict, Any, Optional
import numpy as np
import shap

from app.schemas.shap import (
    ShapFeatureContribution,
    ShapLocalExplanationResponse,
    ShapGlobalFeatureImportanceItem,
    ShapGlobalSummaryResponse,
)
from app.ml.model_trainer import MLRiskModelTrainer
from app.ml.feature_extractor import RiskFeatureExtractor


class ShapExplainerService:
    _explainer = None
    _cached_global_summary = None

    HUMAN_EXPLANATIONS = {
        "feat_ghost_worker_ratio": "Presence of ghost workers credited with wage disbursements but 0 shifts on muster roll.",
        "feat_wage_violation_rate": "Workers compensated below statutory National Floor Wage / State Minimum Wage rates.",
        "feat_hazardous_process": "Operating Schedule I hazardous chemical/industrial processes under OSHWC Code.",
        "feat_contract_ratio": "Elevated reliance on third-party outsourced contractor labour.",
        "feat_missing_register_ratio": "Failure to maintain statutory Form A, Form B, Form C, or Form D registers.",
        "feat_ot_violation_rate": "Overtime hours compensated below double the regular rate under Section 14.",
        "feat_disbursement_mismatch_score": "Mathematical variance between Form B net wages and bank payment UTR totals.",
        "feat_contractor_suppression_score": "Physical factory gate turnstiles reveal workforce exceeding statutory Form A muster.",
        "feat_contract_x_hazardous": "Synergistic risk compound: High contract workforce in hazardous chemical operating environments.",
        "feat_composite_violation_index": "Aggregated density of primary statutory labour code infractions.",
        "feat_composite_anomaly_index": "Aggregated density of cross-document muster and payment discrepancies.",
        "feat_log_workforce": "Scale of workforce expands the scope and liability of systemic non-compliance.",
        "feat_sector_risk_weight": "Inherent historical risk weight of the industrial sector.",
        "feat_prior_inspection_violations": "Unresolved statutory default notices issued in the preceding 24 months.",
        "feat_worker_grievance_rate": "Formal grievances escalated to labour commissioner or conciliation officer.",
        "feat_deduction_breach_rate": "Total deductions surpassing the 50% statutory threshold under Section 18.",
        "feat_inspection_recency_penalty": "Extended duration without physical inspection audit oversight.",
        "feat_workforce_x_missing_registers": "Compounded vulnerability: Substantial workforce without statutory record transparency.",
        "feat_wage_x_disbursement_discrepancy": "Co-occurrence of sub-minimum wages alongside bank payout skimming.",
        "feat_ghost_x_contract_ratio": "High contractor turnover directly linked to phantom payroll vulnerabilities.",
        "feat_female_ratio": "Female workforce proportion and associated welfare provisions under labour codes.",
    }

    @classmethod
    def get_tree_explainer(cls):
        """Initializes or returns cached TreeSHAP explainer for champion XGBoost model."""
        if cls._explainer is None:
            bundle = MLRiskModelTrainer.load_champion_model()
            reg_model = bundle["reg_model"]
            cls._explainer = shap.TreeExplainer(reg_model)
        return cls._explainer

    @classmethod
    def explain_establishment(
        cls,
        establishment_id: str = "EST-001",
        worker_count: Optional[int] = None,
        contract_worker_ratio: Optional[float] = None,
        hazardous_process: Optional[bool] = None,
        industry_sector: Optional[str] = None,
        wage_violation_count: Optional[int] = None,
        ot_violation_count: Optional[int] = None,
        deduction_violation_count: Optional[int] = None,
        missing_register_count: Optional[int] = None,
        ghost_worker_count: Optional[int] = None,
        uncompensated_worker_count: Optional[int] = None,
        disbursement_mismatch_count: Optional[int] = None,
    ) -> ShapLocalExplanationResponse:
        """
        Computes local Shapley feature attribution values (TreeSHAP) for a specific establishment.
        Formula: Predicted Score = Base Value + sum(phi_i)
        """
        bundle = MLRiskModelTrainer.load_champion_model()
        f_names = bundle["feature_names"]
        defn_map = {d.name: d for d in RiskFeatureExtractor.get_feature_definitions()}

        # 1. Extract feature vector
        feat_res = RiskFeatureExtractor.extract_features(
            establishment_id=establishment_id,
            worker_count=worker_count if worker_count is not None else 420,
            contract_worker_ratio=contract_worker_ratio if contract_worker_ratio is not None else 0.42,
            hazardous_process=hazardous_process if hazardous_process is not None else True,
            industry_sector=industry_sector or "Automobile & Auto Components",
            wage_violation_count=wage_violation_count if wage_violation_count is not None else 3,
            ot_violation_count=ot_violation_count if ot_violation_count is not None else 2,
            deduction_violation_count=deduction_violation_count if deduction_violation_count is not None else 1,
            missing_register_count=missing_register_count if missing_register_count is not None else 2,
            ghost_worker_count=ghost_worker_count if ghost_worker_count is not None else 1,
            uncompensated_worker_count=uncompensated_worker_count if uncompensated_worker_count is not None else 1,
            disbursement_mismatch_count=disbursement_mismatch_count if disbursement_mismatch_count is not None else 1,
        )

        x_vec = np.array([[feat_res.vector[fn] for fn in f_names]], dtype=np.float32)

        # 2. Run TreeSHAP
        explainer = cls.get_tree_explainer()
        shap_vals = explainer.shap_values(x_vec)[0]
        base_val = float(explainer.expected_value)

        # 3. Model predicted risk score
        reg_model = bundle["reg_model"]
        pred_score = float(reg_model.predict(x_vec)[0])
        pred_score = round(min(max(10.0, pred_score), 99.0), 1)
        base_val = round(base_val, 1)

        contributions: List[ShapFeatureContribution] = []
        for idx, fn in enumerate(f_names):
            sv = round(float(shap_vals[idx]), 2)
            raw_v = round(float(x_vec[0, idx]), 3)
            defn = defn_map.get(fn)
            label = defn.label if defn else fn
            category = defn.category.value if defn else "UNKNOWN"
            explanation = cls.HUMAN_EXPLANATIONS.get(fn, f"Factor attribution of {label}.")

            contributions.append(
                ShapFeatureContribution(
                    feature_name=fn,
                    feature_label=label,
                    category=category,
                    feature_value=raw_v,
                    shap_value=sv,
                    direction="positive" if sv >= 0 else "negative",
                    explanation=explanation,
                )
            )

        # Separate escalators and mitigators
        positive = sorted([c for c in contributions if c.shap_value > 0.05], key=lambda x: x.shap_value, reverse=True)
        negative = sorted([c for c in contributions if c.shap_value < -0.05], key=lambda x: x.shap_value)

        net_adjustment = round(sum(c.shap_value for c in contributions), 1)

        return ShapLocalExplanationResponse(
            establishment_id=establishment_id,
            base_value=base_val,
            predicted_risk_score=pred_score,
            net_shap_adjustment=net_adjustment,
            positive_escalators=positive,
            negative_mitigators=negative,
            all_contributions=contributions,
        )

    @classmethod
    def compute_global_importance(cls, max_samples: int = 150) -> ShapGlobalSummaryResponse:
        """
        Computes mean absolute SHAP value for each feature across sample establishments
        to discover top global compliance risk drivers.
        """
        if cls._cached_global_summary:
            return cls._cached_global_summary

        bundle = MLRiskModelTrainer.load_champion_model()
        f_names = bundle["feature_names"]
        defn_map = {d.name: d for d in RiskFeatureExtractor.get_feature_definitions()}

        X_raw, _, _ = RiskFeatureExtractor.extract_matrix_from_dataset()
        X_sample = np.array(X_raw[:max_samples], dtype=np.float32)

        explainer = cls.get_tree_explainer()
        shap_vals_matrix = explainer.shap_values(X_sample)

        mean_abs = np.mean(np.abs(shap_vals_matrix), axis=0)

        items: List[ShapGlobalFeatureImportanceItem] = []
        for idx, fn in enumerate(f_names):
            score = round(float(mean_abs[idx]), 3)
            defn = defn_map.get(fn)
            items.append(
                ShapGlobalFeatureImportanceItem(
                    feature_name=fn,
                    feature_label=defn.label if defn else fn,
                    category=defn.category.value if defn else "UNKNOWN",
                    mean_abs_shap=score,
                    rank=0,
                )
            )

        items = sorted(items, key=lambda x: x.mean_abs_shap, reverse=True)
        for i, item in enumerate(items):
            item.rank = i + 1

        cls._cached_global_summary = ShapGlobalSummaryResponse(
            dataset_size=len(X_sample),
            feature_count=len(items),
            top_features=items,
        )
        return cls._cached_global_summary
