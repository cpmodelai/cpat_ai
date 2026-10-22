from typing import Union, List, Dict, Tuple

import pandas as pd

def is_value_notna(
        x: Union[List[str], str, int]
        ) -> bool:
    """
    """
    if isinstance(x, list):
        return bool(x)
    return pd.notna(x)

def get_scenarios(
        scenarios: pd.DataFrame
        ) -> Tuple[
            List[Dict[str, Union[List[str], str, int]]],
            List[str]
            ]:
    """
    """
    unique_countries_sets = scenarios['SelectedCountries'].unique()
    scenarios = scenarios.drop(columns=['SelectedCountries'])
    # TODO change logic to tuples?
    scenarios = scenarios.assign(
        SelectedSectors=lambda x: x['SelectedSectors'].apply(list),
        SelectedFuels=lambda x: x['SelectedFuels'].apply(list)
    )
    list_of_scenarios = [
        {k: v for k, v in row.items() if is_value_notna(v)}
        for row in scenarios.to_dict(orient='records')
    ]
    # TODO schemat validation
    # TODO validate scenarios for values (same countries, etc)
    # TODO load results config

    return list_of_scenarios, list(unique_countries_sets[0])
