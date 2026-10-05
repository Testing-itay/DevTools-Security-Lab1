"""XGBoost and CatBoost predictors for security classification."""

import numpy as np
import xgboost as xgb
from catboost import CatBoostClassifier


def create_xgb_classifier(n_estimators: int = 100) -> xgb.XGBClassifier:
    """Create XGBoost classifier for binary security classification."""
    return xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )


def create_catboost_classifier(iterations: int = 100) -> CatBoostClassifier:
    """Create CatBoost classifier for vulnerability prediction."""
    return CatBoostClassifier(
        iterations=iterations,
        depth=6,
        learning_rate=0.1,
        random_seed=42,
        verbose=0,
    )


def ensemble_predict(
    X: np.ndarray,
    xgb_model: xgb.XGBClassifier,
    cat_model: CatBoostClassifier,
) -> np.ndarray:
    """Combine XGBoost and CatBoost predictions via majority vote."""
    xgb_pred = xgb_model.predict(X)
    cat_pred = cat_model.predict(X)
    return np.round((xgb_pred + cat_pred) / 2).astype(int)
