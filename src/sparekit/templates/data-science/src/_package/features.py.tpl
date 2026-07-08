"""Feature engineering helpers."""

from __future__ import annotations

import pandas as pd


def add_ratio_feature(df: pd.DataFrame, numerator: str, denominator: str, output: str) -> pd.DataFrame:
    """Return a copy of df with a safe ratio feature."""

    result = df.copy()
    result[output] = result[numerator] / result[denominator].replace(0, pd.NA)
    return result
