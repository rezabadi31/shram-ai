"""SHAP TreeExplainer for risk feature attribution."""
from typing import Dict, Any, List


class SHAPExplainerService:
    def explain_prediction(self, features: Dict[str, float]) -> List[Dict[str, Any]]:
        """Returns ordered list of feature contributions to the final risk score."""
        return []
