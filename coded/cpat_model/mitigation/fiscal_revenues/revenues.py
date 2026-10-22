import pandas as pd

import cpat_model.constants as c

# [Post policy GDP]

def get_total_revenues_change(
        total_revenues_additional: pd.DataFrame, # (c)
        year: int
        ) -> pd.DataFrame: # (c)
    """
    'Fiscal revenues raised (% GDP), change from previous  year' (v361)
    CPAT Excel: baseline 6371, scenario 11361

    returns dims (c), t
    """
    # get structure for the current year
    total_revenues_change = total_revenues_additional.loc[:, str(year)].copy()

    total_revenues_change = (
        total_revenues_additional.loc[:, str(year)]
        - total_revenues_additional.loc[:, str(year - 1)]
    )

    return total_revenues_change


def get_total_revenues_additional(
        scenario_type: str,
        total_revenues_per_gdp_baseline: pd.DataFrame, # (c)
        total_revenues_per_gdp: pd.DataFrame = pd.DataFrame() # (c)
        ) -> pd.DataFrame: # (c)
    """
    'Fiscal revenues raised (% GDP), change from previous  year' (v361)
    CPAT Excel: baseline 6370, scenario 11360

    total_revenues_per_gdp - from current scenario
    total_revenues_per_gdp_baseline - from baseline

    returns dims (c), t
    """
    # TODO: result from this f should be concatenated to previous years
    # as we need to pass t and t-1 into the next f
    if scenario_type == c.BASELINE:
        return total_revenues_per_gdp_baseline - total_revenues_per_gdp_baseline
    return total_revenues_per_gdp - total_revenues_per_gdp_baseline


def get_total_revenues_per_gdp(
        total_revenues: pd.DataFrame, # (c)
        real_baseline_gdp: pd.DataFrame, # (c)
        ) -> pd.DataFrame: # (c)
    """
    'Total revenues %GDP' (v361)
    CPAT Excel: baseline 6363, scenario 11353

    returns dims (c), t
    """
    return total_revenues / real_baseline_gdp


def get_total_revenues(
        r_fuel_revenues: pd.DataFrame,
        # r_additional_excise: pd.DataFrame,
        r_existing_taxes: pd.DataFrame,
        r_vat: pd.DataFrame,
        r_losses: pd.DataFrame,
        # r_renewable_cost: pd.DataFrame,
        r_methane_fee: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'Total revenues' (v361)
    CPAT Excel: baseline 6362, scenario 11352

    returns dims (c), t
    """
    total_revenues = (
        r_fuel_revenues + r_existing_taxes + r_vat + r_losses + r_methane_fee
    )

    return total_revenues
