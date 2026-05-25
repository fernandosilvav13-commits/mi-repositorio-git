import re
import logging
from typing import Literal

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from app.schemas.classification import ClassificationResult, DocumentCategory
from app.data.training_samples import TRAINING_SAMPLES

logger = logging.getLogger(__name__)

CLASSIFICATION_THRESHOLD = 0.7
CATEGORIES: list[DocumentCategory] = ["cv", "non-cv"]


class DocClassifier:
    def __init__(self):
        self._vectorizer: TfidfVectorizer | None = None
        self._classifier: CalibratedClassifierCV | None = None
        self._categories: list[DocumentCategory] = CATEGORIES
        self._fitted = False

    def _build_vectorizer(self) -> TfidfVectorizer:
        return TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            lowercase=True,
            strip_accents="unicode",
            analyzer="word",
            token_pattern=r"(?u)\b\w+\b",
        )

    def _preprocess_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    def _fit(self) -> None:
        texts = [self._preprocess_text(s["text"]) for s in TRAINING_SAMPLES]
        labels = [s["label"] for s in TRAINING_SAMPLES]

        self._vectorizer = self._build_vectorizer()
        X = self._vectorizer.fit_transform(texts)

        base_svm = LinearSVC(class_weight="balanced", max_iter=2000, dual="auto")
        self._classifier = CalibratedClassifierCV(base_svm, cv=3)
        self._classifier.fit(X, labels)
        self._fitted = True
        logger.info(
            "DocClassifier trained on %d samples (%d CV, %d non-CV)",
            len(texts),
            sum(1 for l in labels if l == "cv"),
            sum(1 for l in labels if l == "non-cv"),
        )

    def predict(self, text: str) -> DocumentCategory:
        if not self._fitted:
            self._fit()
        cleaned = self._preprocess_text(text)
        X = self._vectorizer.transform([cleaned])
        pred = self._classifier.predict(X)[0]
        return pred

    def predict_proba(self, text: str) -> dict[str, float]:
        if not self._fitted:
            self._fit()
        cleaned = self._preprocess_text(text)
        if not cleaned:
            return {cat: 0.0 for cat in self._categories}
        X = self._vectorizer.transform([cleaned])
        probs = self._classifier.predict_proba(X)[0]
        return dict(zip(self._categories, probs))

    def classify(
        self, text: str, threshold: float = CLASSIFICATION_THRESHOLD
    ) -> ClassificationResult:
        cleaned = self._preprocess_text(text)
        if not cleaned:
            return ClassificationResult(
                category="non-cv",
                confidence=0.0,
                top_categories=[
                    {"category": "non-cv", "confidence": 0.0},
                    {"category": "cv", "confidence": 0.0},
                ],
            )
        probs = self.predict_proba(text)
        max_category = max(probs, key=probs.get)
        max_prob = probs[max_category]
        sorted_cats = sorted(probs.items(), key=lambda x: -x[1])
        top_categories = [
            {"category": cat, "confidence": round(conf, 4)}
            for cat, conf in sorted_cats[:2]
        ]
        if max_prob >= threshold:
            return ClassificationResult(
                category=max_category,
                confidence=round(max_prob, 4),
                top_categories=top_categories,
            )
        return ClassificationResult(
            category="non-cv",
            confidence=round(max_prob, 4),
            top_categories=top_categories,
        )


doc_classifier: DocClassifier = DocClassifier()
