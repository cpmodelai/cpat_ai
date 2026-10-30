"""Policy paths (equation list M1.1)."""
import numpy as np


def path(years, start_year, target_year, start_level, target_level, hold=True):
    """EQ-M1.1  Linear path from start_level in start_year to target_level in target_year, 0 before start_year;
    after target_year held flat (hold=True, Excel-AI's held path) or continued linearly.

    Lambda(t; T0, T1, x0, x1) = x0 + (x1 - x0) (t - T0) / max(T1 - T0, 1)   for t >= T0
    """
    t = np.asarray(years, dtype=float)
    tt = np.minimum(t, target_year) if hold else t
    span = max(target_year - start_year, 1)
    value = start_level + (target_level - start_level) * (tt - start_year) / span
    return np.where(t < start_year, 0.0, value)
