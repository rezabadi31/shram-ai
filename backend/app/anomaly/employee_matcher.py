"""Fuzzy and exact employee identifier matching."""
from typing import Dict, Any, List


class EmployeeMatcher:
    def match_records(self, primary_list: List[Dict[str, Any]], comparison_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {"matched": [], "unmatched": []}
