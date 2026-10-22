from typing import Dict, Tuple, List

import pandas as pd
import numpy as np

import cpat_model.constants as cnst

# [Post policy GDP]

def get_revenues_allocated(
        revenues_allocation: pd.DataFrame, # (r), just 1 t!
        total_revenues_change: pd.DataFrame, # (c)
        selected_countries: List[str]
        ) -> pd.DataFrame:
    """
    'Revenues allocated (as %GDP)' (v361)
    CPAT Excel: baseline 6381:6388, scenario 11371:11378
    returns dims (c, revenues), t
    """
    # get structure
    revenues_allocated = revenues_allocation.reset_index()

    # extend global demand by country dim
    revenues_allocated_per_country = []
    for country_code in selected_countries:
        revenues_allocated_per_country.append(
            revenues_allocated.assign(
                **{cnst.COUNTRY_CODE: country_code}
            ).set_index([cnst.COUNTRY_CODE, cnst.REVENUES_CODE])
        )
    revenues_allocated = pd.concat(revenues_allocated_per_country)

    # add revenues index level to total_revenues_change
    new_index = (
        pd.MultiIndex.from_product(
            [total_revenues_change.index, cnst.REVENUES_ORDER],
            names=[cnst.COUNTRY_CODE, cnst.REVENUES_CODE]
        )
    )
    total_revenues_change = (
        total_revenues_change
        .reindex(
            total_revenues_change.index.repeat(len(cnst.REVENUES_ORDER))
        )
    )
    total_revenues_change.index = new_index

    revenues_allocated = revenues_allocated * total_revenues_change

    return revenues_allocated


def get_revenues_allocation(
        revenues_recycled: Dict[str, int],
        cp_intro: int,
        simulation_years: Tuple[int]
        ) -> pd.DataFrame: # (r)
    """
    'Allocation of revenues' (v361)
    CPAT Excel: (baseline 1783:1787, scenario 6773:6777) -> 98:102
    
    Rest of the codes added either with 0s or -1
    for dims and to make calculating revenues_allocated easier

    returns dims (revenues), t
    """
    # in % so return / 100
    # one df for all countries

    # assertion for keys
    valid_keys = {cnst.PIT, cnst.CIT, cnst.CAPT, cnst.GNFS, cnst.TRNS}
    assert set(revenues_recycled.keys()) == valid_keys, (
        f"'Revenues recycled' must be exactly: {valid_keys}"
    )

    years = np.arange(simulation_years[0], simulation_years[1] + 1).astype(str)
    revenues_allocation = (
        pd.DataFrame(0.0, index=revenues_recycled.keys(), columns=years, dtype=float)
    )

    for key, value in revenues_recycled.items():
        if value != 0:
            mask = revenues_allocation.columns.astype(float) >= cp_intro
            revenues_allocation.loc[key, mask] = value / 100

    revenues_allocation = (
        pd.concat([
            pd.DataFrame(-1.0, index=[cnst.EXC], columns=years),
            pd.DataFrame(0.0, index=[cnst.VAT], columns=years),
            pd.DataFrame(0.0, index=[cnst.WAGE], columns=years),
            revenues_allocation
        ])
    )
    revenues_allocation: pd.DataFrame = revenues_allocation.loc[cnst.REVENUES_ORDER]

    revenues_allocation.index.name = cnst.REVENUES_CODE

    return revenues_allocation
