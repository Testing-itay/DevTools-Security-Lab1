"""scikit-learn pipeline for code analysis classification."""

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def build_classification_pipeline() -> Pipeline:
    """Build a sklearn Pipeline with StandardScaler and RandomForestClassifier."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )


def train_and_evaluate(X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
    """Train pipeline using train_test_split and return fitted model and score."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    pipeline = build_classification_pipeline()
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    return pipeline, score
