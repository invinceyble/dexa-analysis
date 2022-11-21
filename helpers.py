import os

import numpy as np
import pandas as pd

from consts import Column


def is_local():
    """True if app is running locally."""
    return os.path.isfile(".local")


def validate_uploaded_file(df: pd.DataFrame) -> None:
    for key, var in vars(Column).items():
        if key.startswith("__"):
            continue
        assert var in set(df.columns), var


def to_string(dt: np.datetime64) -> str:
    return np.datetime_as_string(dt, unit="D")
