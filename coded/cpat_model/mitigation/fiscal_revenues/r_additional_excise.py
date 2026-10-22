import pandas as pd

from cpat_model.constants import COUNTRY_CODE

# [Post policy GDP]

def get_r_additional_excise(
        r_additional_excise_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    Totals for '{policy_name} policy - additional excise tax raised by fuel and sector' (v361)
    CPAT Excel: baseline 6220, scenario 11210

    returns dims (c), t
    """

    r_additional_excise = (
        r_additional_excise_by_fuel
        .groupby(level=[COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_additional_excise

def get_r_additional_excise_by_fuel():
    """
    '{policy_name} policy - additional excise tax raised by fuel and sector' (v361)
    CPAT Excel: baseline 6206:6218, scenario 11196:11208

    returns dims (c, sg?, f), t
    """
    # TODO: to be coded after implementation of ntx
    pass
