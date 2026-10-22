import pandas as pd
import numpy as np

import cpat_model.constants as c

from cpat_model.mitigation.ch4.ch4 import PRICE, AVG_POW, PRODUCTION, PERCENT, PER_OTHER

from cpat_model.mitigation.methan_fee.constants import (
    POPULATION_ELASTICITIES, PER_CAPITA_INCOME_ELASTICITIES, ELASTICITY_DEMAND_AGR,
    PASS_THROUGH_MAETHAN_FEE, IS_METHAN_FEE_AGR, METHANE_NON_FOSSIL, REDUCTION_IN_INTENSITY_AGR
)

# [Post policy GDP]

def get_r_agriculture(
        r_agr: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'Agriculture - revenue collection from methane fee' (v361)
    CPAT Excel: rows baseline: 4474; scenario: 9464

    returns dims (c), t
    """
    r_agriculture = (
        r_agr
        .groupby(level=[c.COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_agriculture

def get_r_agr(
        em_ch4_agr: pd.DataFrame,
        mf_non_fossil: pd.DataFrame,
        is_methan_fee_agr: bool = IS_METHAN_FEE_AGR
        ) -> pd.DataFrame:
    """
    'Livestock - revenue collection from methane fee'
    and
    'Rice - revenue collection from methane fee' (v361)
    CPAT Excel: rows baseline: 4465, 4468; scenario: 9455, 9458

    returns dims c, f: (liv, ric), t
    """
    # logic from baseline: 4407 4422, scenario: 9397 9412
    if is_methan_fee_agr:
        return (
            em_ch4_agr * mf_non_fossil.iloc[0] / 1e3
        )

    # if False -> just 0s
    r_agr = em_ch4_agr.copy()
    r_agr.loc[:, :] = 0.0
    return r_agr


def get_em_ch4_agr(
        agr_production: pd.DataFrame,
        ef_ch4_after_abatement: pd.DataFrame,
        # selected_countries: list[str]
        ) -> pd.DataFrame:
    """
    'Livestock - CH4 emissions' and 'Rice - CH4 emissions' (v361)
    CPAT Excel: rows baseline: 4464, 4467; scenario: 9454, 9457

    returns dims c, f: (liv, ric), t
    """
    # TODO:
    # if country_code in ['WAV', 'WMR']:
    #     em_ch4_agr(t) = 0

    return agr_production * ef_ch4_after_abatement / 1e6


def get_agr_production(
        production_t0: pd.DataFrame, # ch4_data[PRODUCTION]
        population_growth: pd.DataFrame, # just one t
        gdp_growth_per_capita: pd.DataFrame,
        d_producer_prices: pd.DataFrame,
        simulation_years: tuple[int, int],
        year: int,
         # no agr_production for t0, otherwise just t - 1
        agr_production: pd.DataFrame = pd.DataFrame(),
        ) -> pd.DataFrame:
    """
    'Livestock - production' and 'Rice - production' (v361)
    CPAT Excel: rows baseline: 4459, 4460; scenario: 9449, 9450

    returns dims c, f: (liv, ric), t
    """
    # TODO: agr_production in structure, so we have the whole df held
    # and simplify this
    # for t0 we need to create agr_production
    if year == simulation_years[0]:
        return production_t0.loc[
            ~production_t0.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ].rename(columns={PRODUCTION: str(year)})

    # extend index from (c) to (c, f)
    population_growth_expanded = (
        population_growth
        .reindex(agr_production.index, level=c.COUNTRY_CODE)
    )
    gdp_growth_per_capita_expanded = (
        gdp_growth_per_capita
        .reindex(agr_production.index, level=c.COUNTRY_CODE)
    )

    return (
        agr_production[str(year - 1)]
        * (1 + gdp_growth_per_capita_expanded) ** PER_CAPITA_INCOME_ELASTICITIES[c.AGR]
        * (1 + population_growth_expanded) ** POPULATION_ELASTICITIES[c.AGR]
        * d_producer_prices[str(year)] ** ELASTICITY_DEMAND_AGR
    ).to_frame(name=str(year))


def get_d_producer_prices(
        mf_agr: pd.DataFrame,
        ch4_price: pd.DataFrame, # ch4_data[PRICE]
        simulation_years: tuple[int, int],
        pass_through_methane_fee: float = PASS_THROUGH_MAETHAN_FEE
        ) -> pd.DataFrame:
    """
    'Crude oil - change in producer prices, caused by methane fee'
    and 'Coal - change in producer prices, caused by methane fee' (v361)
    CPAT Excel: rows baseline: 4453, 4454; scenario: 9443, 9444

    For further transformations:
        Crude oil indexed as liv
        Coal indexed as ric

    returns dims c, f: (liv, ric), all t
    """
    year_0 = simulation_years[0]
    d_producer_prices = mf_agr.copy()
    d_producer_prices.loc[:, str(year_0)] = 1.0

    pass_through = 1 - pass_through_methane_fee

    for year in range(year_0 + 1, simulation_years[1] + 1):
        d_producer_prices[str(year)] = (
            1
            + (mf_agr.loc[:, str(year)] - mf_agr.loc[:, str(year - 1)])
            / ch4_price.loc[:, PRICE] * pass_through
        )

    return d_producer_prices


def get_mf_agr(
        ef_ch4_after_abatement: pd.DataFrame,
        mf_non_fossil: pd.DataFrame,
        is_methan_fee_agr: bool = IS_METHAN_FEE_AGR
        ) -> pd.DataFrame:
    """
    'Methane fee - livestock' and 'Methane fee - rice' (v361)
    CPAT Excel: rows baseline: 4412, 4427; scenario: 9402, 9417

    returns dims c, f: (liv, ric), all t
    """
    assert (
        ef_ch4_after_abatement.columns.equals(mf_non_fossil.columns)
    ), "Columns do not match: ef_ch4_after_abatement and mf_non_fossil"

    # logic from baseline: 4407 4422, scenario: 9397 9412
    if is_methan_fee_agr:
        return ef_ch4_after_abatement * mf_non_fossil.iloc[0]

    mf_agr = ef_ch4_after_abatement.copy()
    mf_agr.loc[:, :] = 0.0
    return mf_agr


def get_ef_ch4_after_abatement(
        ef_ch4_baseline: pd.DataFrame,
        ef_ch4_baseline_reduction: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'CH4 emissions factor, after abatement' (v361)
    CPAT Excel: rows baseline: 4411, 4426; scenario: 9401, 9416

    returns dims c, f: (liv, ric), all t
    """
    assert (
        ef_ch4_baseline.columns.equals(ef_ch4_baseline_reduction.columns)
    ), "Columns do not match: ef_ch4_baseline and ef_ch4_baseline_reduction"
    assert (
        ef_ch4_baseline.index.equals(ef_ch4_baseline_reduction.index)
    ), "Index does not match: ef_ch4_baseline and ef_ch4_baseline_reduction"

    return (
        (1 - ef_ch4_baseline_reduction)
        * ef_ch4_baseline
    )


def get_ef_ch4_baseline_reduction(
        mf_non_fossil: pd.DataFrame,
        avg_pow: pd.DataFrame # ch4_data[AVG_POW]
        ) -> pd.DataFrame:
    """
    'CH4 emissions factor, baseline reduction' (v361)
    CPAT Excel: rows baseline: 4409, 4424; scenario: 9399, 9414

    returns dims c, f: (liv, ric), all t
    """
    mf_values = mf_non_fossil.values[0]
    years = mf_non_fossil.columns

    avg_pow_filtered = (
        avg_pow[avg_pow.index.get_level_values(c.FUEL_CODE).isin([c.LIV, c.RIC])]
    )

    mf_values_matrix = np.tile(mf_values, (avg_pow_filtered.shape[0], 1))

    avg_pow_a = avg_pow_filtered[f'{AVG_POW}_a'].values[:, np.newaxis]
    avg_pow_b = avg_pow_filtered[f'{AVG_POW}_b'].values[:, np.newaxis]

    result = avg_pow_a * np.power(mf_values_matrix, avg_pow_b)
    result = np.clip(result, 0, 1) # max(0, min(1, result))

    return pd.DataFrame(result, index=avg_pow_filtered.index, columns=years)


def get_ef_ch4_baseline(
        methane_em_intensity_by_source: pd.DataFrame,
        simulation_years: tuple[int, int]
        ) -> pd.DataFrame:
    """
    'CH4 emissions factor, baseline' ->
    'Emission factors, agriculture and waste, ch4' (v361)
    CPAT Excel: rows baseline: 4400, 4415; scenario: 9390, 9405
    baseline, scenario -> 1574 (liv), 1575 (ric)

    returns dims c, f: (liv, ric), all t
    """
    # methane_em_by_source -> methane_em_intensity_by_source is up to 2022
    # take all t that we obtain based on DB
    ef_ch4_baseline = methane_em_intensity_by_source.copy()

    last_db_year = methane_em_intensity_by_source.columns.astype(int).max()
    d = 1 - REDUCTION_IN_INTENSITY_AGR

    for year in range(last_db_year + 1, simulation_years[1] + 1):
        ef_ch4_baseline[str(year)] = ef_ch4_baseline[str(year - 1)] * d

    return ef_ch4_baseline


def get_methane_em_intensity_by_source(
        methane_em_by_source: pd.DataFrame,
        production_t0: pd.DataFrame # ch4_data[PRODUCTION]
        ) -> pd.DataFrame:
    """
    'Methane emissions by source - livestock and rice' (v361)
    CPAT Excel: rows 896, 897

    returns dims c, f: (liv, ric), all t (same as methane_em_by_source)
    """
    # denominator with protection for division by 0, so we than fillna(0)
    denominator = (
        production_t0.loc[
            ~production_t0.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ]
        [PRODUCTION].replace(0, pd.NA)
    )

    methane_em_intensity_by_source = (
        (methane_em_by_source / METHANE_NON_FOSSIL * 1e6)
        .div(denominator, axis=0)
        .fillna(0)
    )

    return methane_em_intensity_by_source

def get_methane_em_by_source(
        em_allocation_used: pd.DataFrame,
        ghgs_data_agr: pd.DataFrame
        ) -> pd.DataFrame:
    """
    'Methane emissions by source - livestock and rice' (v361)
    CPAT Excel: rows 888, 889

    returns dims c, f: (liv, ric), all t (until 2022 - as in ghgs data)
    """
    ch4_agr = (
        ghgs_data_agr[
            ghgs_data_agr.index.get_level_values(c.GAS).isin([c.CH4])
        ]
        .droplevel(c.GAS)
    )

    methane_em_by_source = pd.concat(
        {
            year: (
                em_allocation_used[PERCENT]
                * em_allocation_used.index.get_level_values(c.COUNTRY_CODE).map(ch4_agr[year])
            )
            for year in ch4_agr.columns
        },
        axis=1
    )

    return methane_em_by_source


def get_em_allocation_used(
        em_allocation_adjusted: pd.DataFrame, # c, (liv, ric)
        em_allocation_avg_adjusted: pd.DataFrame # c, (liv, ric)
        ) -> pd.DataFrame:
    """
    'Emissions allocation percentages - used,
    adjusted to reflect production data and equal 100%' (v361)
    CPAT Excel: K875 (percentages missing), K882, L882

    returns dims c, f: (liv, ric), PERCENT
    """
    # Emissions allocation percentages - selected country, missing
    em_allocation_missing = (
        em_allocation_adjusted
        .groupby(c.COUNTRY_CODE)
        .sum()
        .fillna(0)
    )
    em_allocation_missing[PERCENT] = em_allocation_missing[PERCENT] == 0

    em_allocation_adjusted['missing'] = (
        em_allocation_adjusted.index.get_level_values(c.COUNTRY_CODE)
        .map(em_allocation_missing[PERCENT])
    )
    em_allocation_adjusted['avg'] = em_allocation_avg_adjusted[PERCENT]

    mask = em_allocation_adjusted['missing']
    em_allocation_adjusted.loc[mask, PERCENT] = em_allocation_adjusted.loc[mask, 'avg']

    return em_allocation_adjusted[[PERCENT]]

def get_em_allocation_avg_adjusted(
        production_t0: pd.DataFrame, # ch4_data[PRODUCTION]
        em_allocation_avg: pd.DataFrame # ch4_data[PER_AVG]
        ) -> pd.DataFrame:
    """
    'Emissions allocation percentages - average country,
    adjusted to reflect production data and equal 100%' (v361)
    CPAT Excel: K878:K880, L878:L880

    returns dims c, f: (liv, ric), PERCENT
    """
    ad_to_prod = 'adjusted_to_production'
    ad_to_prod_totals = f'{ad_to_prod}_totals'
    ad_to_100 = 'adjusted_to_100'
    ad_to_100_totals = f'{ad_to_100}_totals'

    em_allocation_avg_total = em_allocation_avg[PERCENT].sum()

    # Emissions allocation percentages - average country, adjusted to equal 100%
    em_allocation_avg_adjusted_to_100 = (
        em_allocation_avg / em_allocation_avg_total
    ).rename(columns={PERCENT: ad_to_100})

    # Emissions allocation percentages - average country, adjusted to reflect production data
    # get structure
    em_allocation_avg_adjusted = (
        production_t0.copy().loc[
            ~production_t0.index.get_level_values(c.FUEL_CODE).isin([c.WST])
        ]
    )
    em_allocation_avg_adjusted[ad_to_100] = (
        em_allocation_avg_adjusted.index.get_level_values(c.FUEL_CODE)
        .map(em_allocation_avg_adjusted_to_100[ad_to_100])
    )
    em_allocation_avg_adjusted[ad_to_prod] = em_allocation_avg_adjusted[ad_to_100]
    mask = em_allocation_avg_adjusted[PRODUCTION] == 0
    em_allocation_avg_adjusted.loc[mask, ad_to_prod] = 0.0


    # Emissions allocation percentages - average country,
    # adjusted to reflect production data and equal 100%
    em_allocation_avg_adjusted[ad_to_100_totals] = (
        em_allocation_avg_adjusted_to_100[ad_to_100].sum()
    )
    em_allocation_avg_adjusted[ad_to_prod_totals] = (
        em_allocation_avg_adjusted
        .groupby(level=c.COUNTRY_CODE)[ad_to_prod]
        .transform('sum')
    )
    # TODO: discuss this -> if ad_to_100_totals == 0, we have 0/0
    mask = em_allocation_avg_adjusted[ad_to_100_totals] == 0.0
    em_allocation_avg_adjusted[PERCENT] = em_allocation_avg_adjusted[PRODUCTION]
    em_allocation_avg_adjusted.loc[mask, PERCENT] = 0.0
    em_allocation_avg_adjusted.loc[~mask, PERCENT] = (
        em_allocation_avg_adjusted.loc[~mask, ad_to_prod]
        / em_allocation_avg_adjusted.loc[~mask, ad_to_prod_totals]
    )

    return em_allocation_avg_adjusted[[PERCENT]]


def get_em_allocation_adjusted(
        em_allocation: pd.DataFrame, # ch4_data[PERCENT]
        em_allocation_other: pd.DataFrame # ch4_data[PER_OTHER]
        ) -> pd.DataFrame:
    """
    'Emissions allocation percentages - selected country, adjusted' (v361)
    CPAT Excel: K874, L874

    returns dims c, f: (liv, ric), PERCENT
    """
    em_allocation_totals = (
        em_allocation
        .groupby(c.COUNTRY_CODE)
        .sum()
    )

    em_allocation['total'] = (
        em_allocation.index.get_level_values(c.COUNTRY_CODE)
        .map(em_allocation_totals[PERCENT])
    )
    em_allocation[PER_OTHER] = (
        em_allocation.index.get_level_values(c.COUNTRY_CODE)
        .map(em_allocation_other[PER_OTHER])
    )

    mask = em_allocation[PERCENT] != 0
    em_allocation.loc[mask, PERCENT] = (
        em_allocation.loc[mask, PERCENT] / em_allocation.loc[mask, 'total']
        * em_allocation.loc[mask, PER_OTHER]
        + em_allocation.loc[mask, PERCENT]
    )
    em_allocation.loc[~mask, PERCENT] = 0.0

    # Drop helper columns
    return em_allocation[[PERCENT]]


def get_mf_non_fossil(
        mf: pd.DataFrame # t
        ) -> pd.DataFrame:
    """
    'Methane fee price trajectory' (v361)
    CPAT Excel: baseline: 1846, scenario: 6836

    returns dims: all t
    """
    return mf * METHANE_NON_FOSSIL

def get_mf(
        mf_price_trajectory: pd.DataFrame, # t
        cp_trajectory: pd.DataFrame, # t
        ct_for_methane: bool = False
        ) -> pd.DataFrame:
    """
    'Methane fee price trajectory' (v361)
    CPAT Excel: baseline: 1844, scenario: 6834

    returns dims: all t
    """
    return mf_price_trajectory + (cp_trajectory * int(ct_for_methane))


def get_mf_price_trajectory(
        scenario_type: str,
        simulation_years: tuple[int, int],
        mf_intro: int,
        mf_outro: int,
        mf_start: int,
        mf_target : int
        ) -> pd.DataFrame:
    """
    'Methane fee price trajectory' (v361)
    CPAT Excel: baseline: 1842, scenario: 6832

    returns dims: all t
    """
    # template with 0s
    years = np.arange(simulation_years[0], simulation_years[1] + 1)
    columns = years.astype(str)
    mf_trajectory = pd.DataFrame([np.zeros(len(columns), dtype=float)], columns=columns)

    if scenario_type == c.BASELINE:
        # return all 0s
        return mf_trajectory

    methan_slope = (mf_target - mf_start) / (mf_outro - mf_intro)
    target_range = years > mf_intro

    mf_trajectory.loc[:, years == mf_intro] = mf_start
    mf_trajectory.loc[:, target_range] = (
            mf_start + (years[target_range] - mf_intro) * methan_slope
        )

    return mf_trajectory
