import pandas as pd

import cpat_model.constants as c

# [Post policy GDP]

def get_r_cost_ren_subsidies(
        r_cost_ren_subsidies_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    Totals for:
    'Cost of renewable subsidies' (v361)
    CPAT Excel: baseline 6329, scenario 11319

    returns dims (c), t
    """

    r_cost_ren_subsidies = (
        r_cost_ren_subsidies_by_fuel
        .groupby(level=[c.COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_cost_ren_subsidies


def get_r_cost_ren_subsidies_by_fuel() -> pd.DataFrame: # (c, f)
    """
    'Used in the calculation - Costs of renewable subsidies come from elasticity-based model' (v361)
    CPAT Excel: baseline 6323:6326, scenario 11313:11316

    returns dims (c), t
    """
    # TODO: implement after elasticity based power model
    pass
