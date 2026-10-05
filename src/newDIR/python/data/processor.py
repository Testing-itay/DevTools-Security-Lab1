"""Data processing with pandas and numpy."""

import pandas as pd
import numpy as np


def normalize_features(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Normalize specified columns using z-score."""
    result = df.copy()
    for col in columns:
        if col in result.columns:
            mean = result[col].mean()
            std = result[col].std()
            result[col] = (result[col] - mean) / std if std > 0 else 0
    return result


def aggregate_by_group(
    df: pd.DataFrame,
    group_col: str,
    agg_cols: dict[str, str],
) -> pd.DataFrame:
    """Aggregate DataFrame by group column with specified aggregations."""
    return df.groupby(group_col).agg(agg_cols).reset_index()


def fill_missing_with_median(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """Fill missing values with column median."""
    result = df.copy()
    for col in numeric_cols:
        if col in result.columns:
            result[col] = result[col].fillna(result[col].median())
    return result
