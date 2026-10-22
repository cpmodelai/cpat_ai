from typing import Callable
import pandas as pd

from cpat_model.indicators.utils.constants import INDICATORS_HEADERS
from cpat_model.constants import BASELINE_SCENARIO

def get_suffix(
    scenario_name: str,
    scenario_no: int
    ) -> str:
    if scenario_name == BASELINE_SCENARIO:
        return '1'
    else:
        return f'2_U{scenario_no}'

def with_indicators_schema(
    unit: str,
    header_key: str
    ) -> Callable[
        [Callable[[pd.DataFrame, str], pd.DataFrame]],
        Callable[[pd.DataFrame, str, int], pd.DataFrame]
        ]:
    def decorator(
        func: Callable[[pd.DataFrame, str], pd.DataFrame]
        ) -> Callable[[pd.DataFrame, str, int], pd.DataFrame]:
        def wrapper(
                df: pd.DataFrame,
                scenario_name: str,
                scenario_no: int
                ) -> pd.DataFrame:
            suffix = get_suffix(scenario_name, scenario_no)
            df = func(df, suffix)
            # dropping IDCols, setting CPATCol as an index and assingning Unit
            df = (
                df
                .reset_index(drop=True)
                .set_index(['CPATCode'])
                .assign(**{'Unit': unit, 'Indicator header': INDICATORS_HEADERS[header_key]})
            )
            # reordering columns
            columns = (
                ['Unit', 'Indicator header'] +
                [col for col in df.columns if col not in ['Unit', 'Indicator header']]
            )
            return df[columns]
        return wrapper
    return decorator
