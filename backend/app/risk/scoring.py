"""Risk scoring and classification service."""
from typing import Dict, Any


class RiskScoringService:
    @staticmethod
    def classify_score(score: float) -> str:
        if score >= 70.0:
            return "HIGH"
        elif score >= 40.0:
            return "MEDIUM"
        return "LOW"

    @classmethod
    def compute_score(cls, probability: float) -> Dict[str, Any]:
        score = round(probability * 100.0, 1)
        return {
            "risk_score": score,
            "risk_category": cls.classify_score(score),
            "priority": "HIGH" if score >= 70.0 else ("MEDIUM" if score >= 40.0 else "LOW"),
        }
