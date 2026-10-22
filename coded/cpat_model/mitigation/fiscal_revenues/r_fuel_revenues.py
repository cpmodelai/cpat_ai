import pandas as pd

import cpat_model.constants as c
from cpat_model.indicators.utils.constants import (
    FOSSIL_FUELS, ALL_SECTORS_FROM_AGG, SECTOR_GROUPS, SECTORS_AGG_TMP
)

# [Post policy GDP]

def get_r_fuel_revenues(
        r_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    Totals for '{policy_name} policy - revenues raised by fuel' (v361)
    CPAT Excel: baseline 6198, scenario 11188

    returns dims (c), t
    """

    r_fuel_revenues = (
        r_by_fuel
        .groupby(level=[c.COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_fuel_revenues

def get_r_by_fuel(
        em_f_totals: pd.DataFrame, # (c, f)
        cov_em_by_fuel: pd.DataFrame, # (c, f),
        cp_trajectory: pd.DataFrame, # only t, TODO changed to c specific
        year: int
        ) -> pd.DataFrame: # (c, f)
    """
    '{policy_name} policy - revenues raised by fuel' (v361)
    CPAT Excel: baseline 6190:6197, scenario 11180:11187

    returns dims (c, f), t
    """
    # for one t at a time

    # TODO: if scenario_type == 'Feebates': r_by_fuel <- 0
    # and take this condition higher up so we don't need to calc all the components if 'Feebates'
    # if scenario_type == 'Feebates':
    #     0

    # TODO: implement bio and elec
    #     if f in [bio]:
    #         bgs - bioethanol (row 4678 -> 3925 -> 3832)
    #         bdi - biodiesel (row 4679 -> 3926 -> 3833)
    #         obf - other biofuels (row 4680 -> 3927 -> 3834)
    #         r_by_fuel(t, bio) = (
    #             ( ec(t, tra, bgs) + ec(t, tra, obf) ) * cov_em(t, tra, gso) * cp_trajectory(t) * ef(tra, gso)
    #             + ec(t, tra, bdi) * cov_em(t, tra, die) * cp_trajectory(t) * ef(tra, die) )
    #         ) / 10^9
    #     if f in [elec]:
    #         r_rebate_ct - Rebate of Carbon Tax (negative) (6314 -> 2492)
    #         r_elec_excise - Electricity Excise (6315 -> 2493)
    #         r_by_fuel(t, elec) = r_rebate_ct(t) + r_elec_excise(t)


    # get a scalar value for cp_trajectory in a given year
    cp_trajectory_value = cp_trajectory.at[0, str(year)]

    r_by_fuel: pd.DataFrame = cov_em_by_fuel.copy()

    r_by_fuel = (
        # TODO: important: check the units (/1000)
        em_f_totals * r_by_fuel * cp_trajectory_value / 1000
    )

    # summing ker and lpg to lpk:
    r_by_fuel = (
        r_by_fuel
        .reset_index()
        .assign(**{
            c.FUEL_CODE: lambda x: x[c.FUEL_CODE].replace({c.KER: c.LPK, c.LPG: c.LPK})
        })
        .groupby([c.COUNTRY_CODE, c.FUEL_CODE], as_index=True)
        .sum()
    )

    return r_by_fuel


def get_cov_em_by_fuel(
        cov_em: pd.DataFrame, # (c, sg, f)
        em_sg_f: pd.DataFrame, # (c, sg, f)
        em_f_totals: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c, f)
    """
    'Covered CO2 emissions by fuel' (v361) - f aggregation
    CPAT Excel: baseline 6128:6169, scenario 11118:11159

    for f in FOSSIL_FUELS

    returns dims (c, f), t
    """
    # for one t at a time

    cov_em_by_fuel = em_sg_f * cov_em

    cov_em_by_fuel = (
        cov_em_by_fuel
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    # if em_f_totals == 0 -> 0
    cov_em_by_fuel = (
        cov_em_by_fuel.where(em_f_totals != 0, 0)
        / em_f_totals
    ).fillna(0)

    return cov_em_by_fuel


def get_cov_em(
        p_cov_f: pd.DataFrame, # (c, f) - 10 fuels
        p_cov_s: pd.DataFrame, # (c, s) - 18 sectors
        ec_sg_f: pd.DataFrame, # sectors aggregated
        ec: pd.DataFrame,
        year: int
        ) -> pd.DataFrame: # (c, sg, f)
    """
    'Covered CO2 emissions by fuel' (v361) - no f aggregation
    CPAT Excel: baseline 6128:6169, scenario 11118:11159

    for f in FOSSIL_FUELS

    returns dims (c, sg, f), t
    """
    # for one t at a time

    # year to str
    year = str(year)

    # filtering for better time complexity
    p_cov_f_filtered = (
        p_cov_f[
            p_cov_f.index.get_level_values(c.FUEL_CODE).isin(FOSSIL_FUELS)
        ]
    )
    p_cov_s_filtered = (
        p_cov_s[
            p_cov_s.index.get_level_values(c.SECTOR_CODE).isin(SECTOR_GROUPS + ALL_SECTORS_FROM_AGG)
        ]
    )
    ec_sg_f_filtered = (
        ec_sg_f[
            ec_sg_f.index.get_level_values(c.SECTOR_CODE).isin(SECTOR_GROUPS)
            & ec_sg_f.index.get_level_values(c.FUEL_CODE).isin(FOSSIL_FUELS)
        ]
    )
    ec_filtered = (
        ec[
            ec.index.get_level_values(c.SECTOR_CODE).isin(ALL_SECTORS_FROM_AGG)
            & ec.index.get_level_values(c.FUEL_CODE).isin(FOSSIL_FUELS)
        ]
    )

    # get structure from ec_sg_f (no bio)
    cov_em = ec_sg_f_filtered.copy()


    # if sg == pow:
    # adding sg column for joins
    p_cov_f_filtered_with_s_col = p_cov_f_filtered.assign(**{c.SECTOR_CODE: c.POW}).reset_index()

    cov_em.loc[pd.IndexSlice[:, c.POW, :], :] = (
        p_cov_f_filtered_with_s_col
        .merge(
            p_cov_s_filtered.loc[pd.IndexSlice[:, c.POW], :].reset_index(),
            how='left',
            on=[c.COUNTRY_CODE, c.SECTOR_CODE],
            suffixes=('_f', '_s')
        )
        .set_index(c.ID_COL_NAMES)
        .assign(**{year: lambda x: x[f'{year}_f'] * x[f'{year}_s']})
        [[str(year)]]  # Select only result column
    )


    # if sg == tra:

    ec_filtered_subsectors = (
        ec_filtered[
            ec_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.TRA])
        ]
    )

    p_cov_s_filtered_with_f_col = (
        p_cov_s_filtered[
            p_cov_s_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.TRA])
        ]
        .reset_index()
        .merge(
            pd.DataFrame({c.FUEL_CODE: FOSSIL_FUELS + [c.JFU]}),
            how="cross"
        )
        .set_index(c.ID_COL_NAMES)
    )

    # no jfu for ker:
    sum_of_products = (
        (
            ec_filtered_subsectors.loc[
                ~ec_filtered_subsectors.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
            ]
            * p_cov_s_filtered_with_f_col.loc[
                ~p_cov_s_filtered_with_f_col.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
            ]
        )
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    # sum for f other than ker times p_cov_f
    cov_em_tra_no_ker = (
        sum_of_products.loc[
            ~sum_of_products.index.get_level_values(c.FUEL_CODE).isin([c.KER])
        ]
        * p_cov_f_filtered.loc[
            ~p_cov_f_filtered.index.get_level_values(c.FUEL_CODE).isin([c.KER])
        ]
    )

    # for ker (with jfu in avi):
    ec_avi_jfu = (
        ec[
            ec.index.get_level_values(c.SECTOR_CODE).isin([c.AVI])
            & ec.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
        ]
    )
    cov_em_avi_jfu = (
        (
            (
                (
                    ec_avi_jfu
                    * p_cov_s_filtered_with_f_col.loc[
                        p_cov_s_filtered_with_f_col.index.get_level_values(
                            c.SECTOR_CODE).isin([c.AVI])
                        & p_cov_s_filtered_with_f_col.index.get_level_values(
                            c.FUEL_CODE).isin([c.JFU])
                    ]
                )
                .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
                .sum(numeric_only=True)
            )
            * p_cov_f[
                p_cov_f.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
            ]
        )
        .rename(index={c.JFU: c.KER}, level=c.FUEL_CODE)
    )


    # includes avi, jfu
    cov_em_tra_ker = (
        (
            sum_of_products.loc[
                sum_of_products.index.get_level_values(c.FUEL_CODE).isin([c.KER])
            ]
            * p_cov_f_filtered.loc[
                p_cov_f_filtered.index.get_level_values(c.FUEL_CODE).isin([c.KER])
            ]
        ).add(cov_em_avi_jfu, fill_value=0)
    )

    ec_sg_filtered_f_filtered = (
        ec_sg_f_filtered.loc[pd.IndexSlice[:, c.TRA, :], :]
        .droplevel(c.SECTOR_CODE)
    )

    cov_em.loc[pd.IndexSlice[:, c.TRA, :], :] = (
        (
            pd.concat(
                [cov_em_tra_no_ker, cov_em_tra_ker]
            ).where(ec_sg_filtered_f_filtered != 0, 0)
            / ec_sg_filtered_f_filtered
        )
        .fillna(0)
        .assign(**{c.SECTOR_CODE: c.TRA})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    # if sg == bld:

    ec_filtered_subsectors = (
        ec_filtered[
            ec_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.BLD])
        ]
    )

    p_cov_s_filtered_with_f_col = (
        p_cov_s_filtered[
            p_cov_s_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.BLD])
        ]
        .reset_index()
        .merge(
            pd.DataFrame({c.FUEL_CODE: FOSSIL_FUELS}),
            how="cross"
        )
        .set_index(c.ID_COL_NAMES)
    )

    sum_of_products = (
        (
            ec_filtered_subsectors
            * p_cov_s_filtered_with_f_col
        )
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    ec_sg_filtered_f_filtered = (
        ec_sg_f_filtered.loc[pd.IndexSlice[:, c.BLD, :], :]
        .droplevel(c.SECTOR_CODE)
    )

    cov_em.loc[pd.IndexSlice[:, c.BLD, :], :] = (
        (
            sum_of_products.where(ec_sg_filtered_f_filtered != 0, 0)
            / ec_sg_filtered_f_filtered
            * p_cov_f_filtered
        )
        .fillna(0)
        .assign(**{c.SECTOR_CODE: c.BLD})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    # if sg == ind:

    ec_filtered_subsectors = (
        ec_filtered[
            ec_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.IND])
        ]
    )

    p_cov_s_filtered_with_f_col = (
        p_cov_s_filtered[
            p_cov_s_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.IND])
        ]
        .reset_index()
        .merge(
            pd.DataFrame({c.FUEL_CODE: FOSSIL_FUELS}),
            how="cross"
        )
        .set_index(c.ID_COL_NAMES)
    )

    sum_of_products = (
        (
            ec_filtered_subsectors
            * p_cov_s_filtered_with_f_col
        )
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    ec_sg_filtered_f_filtered = (
        ec_sg_f_filtered.loc[pd.IndexSlice[:, c.IND, :], :]
        .droplevel(c.SECTOR_CODE)
    )

    cov_em.loc[pd.IndexSlice[:, c.IND, :], :] = (
        (
            sum_of_products.where(ec_sg_filtered_f_filtered != 0, 0)
            / ec_sg_filtered_f_filtered
            * p_cov_f_filtered
        )
        .fillna(0)
        .assign(**{c.SECTOR_CODE: c.IND})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    # if sg == oen: cov_em <- 0
    cov_em.loc[pd.IndexSlice[:, c.OEN, :], :] = 0

    return cov_em
