import re
from typing import List, Dict, Tuple, Optional
from app.schemas.classification import (
    ClassifiedCategory,
    ClassifierStage,
    ClassificationMatchSignal,
    ClassificationResult,
)

# Statutory Keyword and Rule Heuristics
STATUTORY_PATTERNS: Dict[ClassifiedCategory, List[Tuple[str, float]]] = {
    ClassifiedCategory.WAGE_REGISTER: [
        (r"form\s+b\b", 0.98),
        (r"register\s+of\s+wages", 0.95),
        (r"rule\s+78\s*\(\s*1\s*\)\s*\(\s*a\s*\)\s*\(\s*i\s*\)", 0.99),
        (r"minimum\s+wages\s+act", 0.90),
        (r"wage\s+rate", 0.80),
        (r"net\s+payable", 0.85),
        (r"dearness\s+allowance", 0.82),
        (r"basic\s+wage", 0.80),
        (r"gross\s+wage", 0.80),
    ],
    ClassifiedCategory.ATTENDANCE_REGISTER: [
        (r"form\s+d\b", 0.98),
        (r"muster\s+roll", 0.96),
        (r"attendance\s+register", 0.95),
        (r"rule\s+78\s*\(\s*1\s*\)\s*\(\s*a\s*\)\s*\(\s*ii\s*\)", 0.99),
        (r"days\s+worked", 0.82),
        (r"in\s+time\s+out\s+time", 0.85),
        (r"shift\s+timing", 0.80),
        (r"total\s+man\s*days", 0.88),
    ],
    ClassifiedCategory.EMPLOYEE_REGISTER: [
        (r"form\s+a\b", 0.98),
        (r"register\s+of\s+employees", 0.96),
        (r"aadhaar\s+number", 0.85),
        (r"universal\s+account\s+number|\buan\b", 0.90),
        (r"epfo\s+member\s+id", 0.92),
        (r"esic\s+insurance\s+number", 0.92),
        (r"date\s+of\s+joining", 0.82),
        (r"nominee\s+details", 0.84),
    ],
    ClassifiedCategory.PAYROLL: [
        (r"bank\s+payout\s+scroll", 0.96),
        (r"bank\s+disbursement", 0.94),
        (r"salary\s+credit\s+advice", 0.92),
        (r"\butr\s+number\b|\bneft\b|\brtgs\b", 0.90),
        (r"beneficiary\s+account\s+number", 0.88),
        (r"ifsc\s+code", 0.82),
    ],
    ClassifiedCategory.SAFETY_RECORD: [
        (r"safety\s+committee\s+minutes", 0.96),
        (r"factory\s+inspection\s+report", 0.94),
        (r"accident\s+register", 0.95),
        (r"form\s+18\b", 0.98),
        (r"ppe\s+compliance", 0.88),
        (r"occupational\s+health\s+center", 0.89),
        (r"fire\s+extinguisher\s+audit", 0.85),
    ],
    ClassifiedCategory.EMPLOYMENT_CONTRACT: [
        (r"employment\s+agreement", 0.96),
        (r"letter\s+of\s+appointment", 0.95),
        (r"terms\s+and\s+conditions\s+of\s+employment", 0.92),
        (r"probation\s+period", 0.85),
        (r"notice\s+period", 0.84),
    ],
    ClassifiedCategory.RETURN: [
        (r"unified\s+annual\s+return", 0.98),
        (r"annual\s+return", 0.92),
        (r"form\s+25\b|form\s+xxv\b", 0.96),
        (r"shram\s+suvidha\s+portal\s+filing", 0.95),
        (r"calendar\s+year\s+ending", 0.88),
    ],
}

# Statutory Corpus Prototypes for ML Fallback
STATUTORY_CORPUS = {
    ClassifiedCategory.WAGE_REGISTER: "form b register wages basic salary dearness allowance hra overtime deduction net payable rate day employee signature payment remuneration compensation stipend earnings bonus dues",
    ClassifiedCategory.ATTENDANCE_REGISTER: "form d muster roll attendance daily in out time shift present absent earned leave casual leave mandays worked hours head count biometric punches duty",
    ClassifiedCategory.EMPLOYEE_REGISTER: "form a register employees workmen personal details aadhaar uan pf epfo esic insurance date joining designation department father spouse address",
    ClassifiedCategory.PAYROLL: "bank payout scroll salary disbursement neft rtgs utr transaction reference credit account ifsc advice statement bank advice voucher wire",
    ClassifiedCategory.SAFETY_RECORD: "safety committee minutes inspection factory accident register hazard first aid medical checkup fire mock drill oshwc personal protective equipment incident audit",
    ClassifiedCategory.EMPLOYMENT_CONTRACT: "appointment letter employment contract agreement probation period compensation code conduct clause termination notice terms service conditions job offer",
    ClassifiedCategory.RETURN: "unified annual return compliance statutory summary year ending shram suvidha submission inspection declaration annual reporting form xxv",
}


class DocumentClassifierService:
    @classmethod
    def classify(cls, text: str, filename: Optional[str] = None) -> ClassificationResult:
        """
        Two-stage classifier:
        1. Rule-based keyword matching on statutory patterns & Form numbers.
        2. ML TF-IDF Cosine Similarity fallback if rules are below confidence threshold.
        """
        combined_text = f"{filename or ''}\n{text}".lower()
        matched_signals: List[ClassificationMatchSignal] = []
        category_scores: Dict[ClassifiedCategory, float] = {}

        # Stage 1: Deterministic Statutory Pattern Matching
        for category, patterns in STATUTORY_PATTERNS.items():
            for pat, weight in patterns:
                if re.search(pat, combined_text, re.IGNORECASE):
                    matched_signals.append(
                        ClassificationMatchSignal(
                            signal_name=f"RegexMatch:{pat}",
                            matched_pattern=pat,
                            weight=weight,
                        )
                    )
                    category_scores[category] = max(category_scores.get(category, 0.0), weight)

        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            best_score = category_scores[best_category]
            if best_score >= 0.80:
                filtered_signals = [s for s in matched_signals if any(p in s.matched_pattern for p, _ in STATUTORY_PATTERNS[best_category])]
                return ClassificationResult(
                    predicted_category=best_category,
                    confidence=round(best_score, 2),
                    classifier_stage=ClassifierStage.RULE_HEURISTICS,
                    matched_signals=filtered_signals,
                )

        # Stage 2: ML TF-IDF Cosine Similarity Fallback
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            categories = list(STATUTORY_CORPUS.keys())
            corpus_docs = [STATUTORY_CORPUS[c] for c in categories]
            corpus_docs.append(combined_text)

            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(corpus_docs)

            doc_vector = tfidf_matrix[-1]
            prototype_vectors = tfidf_matrix[:-1]

            similarities = cosine_similarity(doc_vector, prototype_vectors)[0]
            best_idx = int(similarities.argmax())
            best_ml_score = float(similarities[best_idx])
            best_ml_category = categories[best_idx]

            if best_ml_score >= 0.15:
                return ClassificationResult(
                    predicted_category=best_ml_category,
                    confidence=round(min(0.89, 0.50 + (best_ml_score * 0.5)), 2),
                    classifier_stage=ClassifierStage.ML_FALLBACK,
                    matched_signals=[
                        ClassificationMatchSignal(
                            signal_name="TF-IDF Cosine Similarity",
                            matched_pattern=f"Similarity score: {best_ml_score:.3f}",
                            weight=round(best_ml_score, 2),
                        )
                    ],
                )
        except Exception:
            pass

        # Fallback: Unknown
        return ClassificationResult(
            predicted_category=ClassifiedCategory.UNKNOWN,
            confidence=0.30,
            classifier_stage=ClassifierStage.RULE_HEURISTICS,
            matched_signals=[],
        )
