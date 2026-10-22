import pandas as pd

# [Post policy GDP]

def get_r_methane_fee(
        r_agriculture: pd.DataFrame,
        r_wst: pd.DataFrame,
        # r_extractives: pd.DataFrame TODO
        ) -> pd.DataFrame:
    """
    'Methane fee - revenue' (v361)
    CPAT Excel: rows baseline: 6336; scenario: 11326

    returns dims (c), t
    """

    return r_agriculture + r_wst
