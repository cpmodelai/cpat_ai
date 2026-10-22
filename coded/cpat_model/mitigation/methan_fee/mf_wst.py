import pandas as pd

import cpat_model.constants as c

from cpat_model.mitigation.ch4.ch4 import PRODUCTION

from cpat_model.mitigation.methan_fee.constants import (
    POPULATION_ELASTICITIES, METHANE_NON_FOSSIL, REDUCTION_IN_INTENSITY_WST, IS_METHAN_FEE_WST
)

# [Post policy GDP]

def get_r_wst(
        mf_wst: pd.DataFrame,
        em_ch4_wst: pd.DataFrame,
        is_methan_fee_wst: bool = IS_METHAN_FEE_WST
        ) -> pd.DataFrame:
    """
    'Waste - revenue collection from methane fee' (v361)
    CPAT Excel: rows baseline: 4471; scenario: 9461

    returns dims c, f: (wst), all t
    """
    # logic from baseline: 4436, scenario: 9426
    if is_methan_fee_wst:
        return (
            em_ch4_wst * mf_wst / 1e3
        )

    # if False -> just 0s
    r_wst = em_ch4_wst.copy()
    r_wst.loc[:, :] = 0.0
    return r_wst


def get_mf_wst(
        ef_ch4_after_abatement_wst: pd.DataFrame,
        mf_non_fossil: pd.DataFrame,
        is_methan_fee_wst: bool = IS_METHAN_FEE_WST
        ) -> pd.DataFrame:
    """
    'Methane fee - waste' (v361)
    CPAT Excel: rows baseline: 4441; scenario: 9431

    returns dims c, f: (wst), all t
    """
    assert (
        ef_ch4_after_abatement_wst.columns.equals(mf_non_fossil.columns)
    ), "Columns do not match: ef_ch4_after_abatement_wst and mf_non_fossil"

    # logic from baseline: 4436, scenario: 9426
    if is_methan_fee_wst:
        return ef_ch4_after_abatement_wst * mf_non_fossil.iloc[0]

    mf_wst = ef_ch4_after_abatement_wst.copy()
    mf_wst.loc[:, :] = 0.0
    return mf_wst


def get_em_ch4_wst(
        wst_production: pd.DataFrame,
        ef_ch4_after_abatement_wst: pd.DataFrame,
        # selected_countries: list[str]
        ) -> pd.DataFrame:
    """
    'Waste - CH4 emissions'(v361)
    CPAT Excel: rows baseline: 4470; scenario: 9460

    returns dims c, f: (wst), all t
    """
    # TODO:
    # if country_code in ['WAV', 'WMR']:
    #     get_em_ch4_wst(t) = 0

    return wst_production * ef_ch4_after_abatement_wst / 1e6


def get_wst_production(
        production_t0: pd.DataFrame, # ch4_data[PRODUCTION]
        population_growth: pd.DataFrame,
        simulation_years: tuple[int, int],
        ) -> pd.DataFrame:
    """
    'Waste production' (v361)
    CPAT Excel: rows baseline: 4461; scenario: 9451

    returns dims c, f: (wst), all t
    """
    production_t0_countries = production_t0.index.unique(level=c.COUNTRY_CODE)
    population_growth_countries = population_growth.index.unique(level=c.COUNTRY_CODE)
    assert (
        production_t0_countries.equals(population_growth_countries)
    ), (
        f"Mismatch in country codes:\n"
        f"production_t0: {list(production_t0_countries)}\n"
        f"population_growth: {list(population_growth_countries)}"
    )
    year_0 = simulation_years[0]

    wst_production_t0 = production_t0.loc[
        production_t0.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ].rename(columns={PRODUCTION: str(year_0)})

    # extend index from (c) to (c, f)
    population_growth_expanded = (
        population_growth
        .reindex(wst_production_t0.index, level=c.COUNTRY_CODE)
    )

    # after transformations population_growth_expanded structure will be retured as wst_production
    population_growth_expanded[str(year_0)] = wst_production_t0.loc[:, str(year_0)]
    for year in range(year_0 + 1, simulation_years[1] + 1):
        population_growth_expanded[str(year)] = (
            population_growth_expanded[str(year - 1)]
            * (1 + population_growth_expanded[str(year)]) ** POPULATION_ELASTICITIES[c.WST]
        )
    return population_growth_expanded


def get_ef_ch4_after_abatement_wst(
        ef_ch4_baseline_wst: pd.DataFrame,
        ef_ch4_baseline_reduction: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'CH4 emissions factor, after abatement' (v361)
    CPAT Excel: rows baseline: 4440; scenario: 9430

    In CPAT Excel ef_ch4_baseline_reduction(liv) is used as proxy for wst

    returns dims c, f: (wst), all t
    """
    ef_ch4_baseline_reduction_wst = (
        ef_ch4_baseline_reduction[
            ef_ch4_baseline_reduction.index.get_level_values(c.FUEL_CODE).isin([c.LIV])
        ]
        .rename(index={c.LIV: c.WST}, level=c.FUEL_CODE)
    )
    assert (
        ef_ch4_baseline_wst.columns.equals(ef_ch4_baseline_reduction_wst.columns)
    ), "Columns do not match: ef_ch4_baseline_wst and ef_ch4_baseline_reduction_wst"
    assert (
        ef_ch4_baseline_wst.index.equals(ef_ch4_baseline_reduction_wst.index)
    ), "Index does not match: ef_ch4_baseline_wst and ef_ch4_baseline_reduction_wst"

    return (
        (1 - ef_ch4_baseline_reduction_wst)
        * ef_ch4_baseline_wst
    )


def get_ef_ch4_baseline_wst(
        methane_em_intensity_by_source_wst: pd.DataFrame,
        simulation_years: tuple[int, int]
        ) -> pd.DataFrame:
    """
    'CH4 emissions factor, baseline' ->
    'Emission factors, agriculture and waste, ch4' (v361)
    CPAT Excel: rows baseline: 4429; scenario: 9419
    baseline, scenario -> 1576(wst)

    returns dims c, f: (wst), all t
    """
    # methane_em_by_source and therefore methane_em_intensity_by_source is up to 2022
    # take all t that we can based on DB
    ef_ch4_baseline_wst = methane_em_intensity_by_source_wst.copy()

    last_db_year = methane_em_intensity_by_source_wst.columns.astype(int).max()
    d = 1 - REDUCTION_IN_INTENSITY_WST

    for year in range(last_db_year + 1, simulation_years[1] + 1):
        ef_ch4_baseline_wst[str(year)] = ef_ch4_baseline_wst[str(year - 1)] * d

    return ef_ch4_baseline_wst


def get_methane_em_intensity_by_source_wst(
        methane_em_by_source_wst: pd.DataFrame,
        production_t0: pd.DataFrame # ch4_data[PRODUCTION]
        ) -> pd.DataFrame:
    """
    'Methane emissions by source - waste' (v361)
    CPAT Excel: row 898

    returns dims c, f: (wst), all t (same as methane_em_by_source_wst)
    """
    # denominator with protection for division by 0, so we than fillna(0)
    denominator = (
        production_t0.loc[
            production_t0.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ]
        [PRODUCTION].replace(0, pd.NA)
    )

    methane_em_intensity_by_source_wst = (
        (methane_em_by_source_wst / METHANE_NON_FOSSIL * 1e6)
        .div(denominator, axis=0)
        .fillna(0)
    )

    return methane_em_intensity_by_source_wst


def get_methane_em_by_source_wst(
        ghgs_data_wst: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'Methane emissions by source - livestock and rice' (v361)
    CPAT Excel: rows 890

    returns dims c, f: (wst), all t (until 2022 - as in ghgs data)
    """
    ch4_wst = (
        ghgs_data_wst[
            ghgs_data_wst.index.get_level_values(c.GAS).isin([c.CH4])
        ]
        .rename_axis(index={c.GAS: c.FUEL_CODE})
        .rename(index={c.CH4: c.WST}, level=c.FUEL_CODE)
    )

    return ch4_wst
