from typing import List, Literal

import pandas as pd

import cpat_model.constants as cnst

from cpat_model.mitigation.fiscal_revenues.utils.constants import CONV_MAPPING_LOSSES

# [Post policy GDP]

def get_r_losses(
        r_losses_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    'Total producer-side subsidies' (v361)
    CPAT Excel: baseline 6286, scenario 11276

    returns dims (c), t
    """

    r_losses = (
        r_losses_by_fuel
        .groupby(level=[cnst.COUNTRY_CODE])
        .sum(numeric_only=True)
    ) * -1

    return r_losses


def get_r_losses_by_fuel(
        subsidized_demand: pd.DataFrame, # (c, f)
        per_unit_subsidies: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c, f)
    """
    'Producer-side subsidies' (v361)
    CPAT Excel: baseline 6282:6285, scenario 11272:11275

    returns dims (c, f), t
    """
    # TODO elec/1000
    r_losses_by_fuel = subsidized_demand * per_unit_subsidies

    return r_losses_by_fuel


def get_per_unit_subsidies(
        ps: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, f)
    """
    'Per-unit subsidies' (v361)
    CPAT Excel: baseline 6276:6279, scenario 11266:11269

    returns dims (c, f), t
    """
    # TODO: elec after elasticity based power model
    per_unit_subsidies = (
        ps[
            ps.index.get_level_values(cnst.SECTOR_CODE).isin([cnst.POW])
            & ps.index.get_level_values(cnst.FUEL_CODE).isin([cnst.COA, cnst.NGA, cnst.GSO])
        ]
        .droplevel(cnst.SECTOR_CODE)
        .rename(index={cnst.GSO: cnst.OIL}, level=cnst.FUEL_CODE)
    )

    return per_unit_subsidies

def get_subsidized_demand(
        global_demand: pd.DataFrame, # (c, f)
        domestic_demand: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c, f)
    """
    'Subsidized demand' (v361)
    CPAT Excel: baseline 6270:6273, scenario 11260:11263

    returns dims (c, f), t
    """
    # TODO: elec after elasticity based power model

    # get structure from global_demand
    subsidized_demand = global_demand.copy()

    # if we decide to get domestic demand for all f, this filtering is necessary
    domestic_demand_filtered = (
        domestic_demand[
            domestic_demand.index.get_level_values(cnst.FUEL_CODE).isin([cnst.COA, cnst.NGA])
        ]
    )

    subsidized_demand.loc[pd.IndexSlice[:, (cnst.COA, cnst.NGA), :], :] = (
        (subsidized_demand.loc[pd.IndexSlice[:, (cnst.COA, cnst.NGA), :], :]
        + domestic_demand_filtered)
        / 2
    )

    # we have only one timestep - one column so we can do this:
    subsidized_demand.iloc[:, 0] *= (
        subsidized_demand.index.get_level_values(cnst.FUEL_CODE)
        .map(CONV_MAPPING_LOSSES)
    )
    # TODO: add elec
    return subsidized_demand


def get_global_demand(
        global_demand_raw: pd.DataFrame,
        selected_countries: List[str],
        # MTInputs, row 105:
        global_energy_demand_scenario: Literal[
            'Stated Policies Scenario',
            'Announced Pledges Scenario',
            'Net Zero Scenario'
        ] = 'Stated Policies Scenario'
        ) -> pd.DataFrame: # (c, f)
    """
    'Global demand' (v361)
    CPAT Excel: baseline 6254:6256, scenario 11244:11246
    TODO: this is the same as global_fuel_demand used loaded in international_prices

    returns dims (c, f), t
    """
    # TODO: remove and use 'global_fuel_demand' from IntPrices
    # for all t -> perform just once
    # based on 'Global demand', starting at rows 6253 and 11243

    global_demand_raw = (
        global_demand_raw[
            global_demand_raw['Scenario'] == global_energy_demand_scenario
        ]
        .drop(columns=['Unit', 'Scenario'])
        .reset_index(drop=True)
    )

    # extend global demand by country dim
    gd_per_country = []
    for country_code in selected_countries:
        gd_per_country.append(
            global_demand_raw.assign(
                **{cnst.COUNTRY_CODE: country_code}
            ).set_index([cnst.COUNTRY_CODE, cnst.FUEL_CODE])
        )
    global_demand = pd.concat(gd_per_country).sort_index()

    return global_demand


def get_domestic_demand(
    ec_f_totals: pd.DataFrame # (c, f)
    ) -> pd.DataFrame: # (c, f)
    """
    'Domestic demand' (v361)
    CPAT Excel: baseline 6265:6267, scenario 11255:11257

    returns dims (c, f), t
    """
    # TODO: elec after elasticity based power model
    domestic_demand = (
        ec_f_totals[
            ec_f_totals.index.get_level_values(cnst.FUEL_CODE).isin([cnst.COA, cnst.NGA])
        ]
    )

    return domestic_demand
