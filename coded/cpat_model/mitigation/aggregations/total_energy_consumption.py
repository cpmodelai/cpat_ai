import pandas as pd

from cpat_model.indicators.utils.constants import SECTORS_AGG_TMP, FOSSIL_FUELS_AND_BIO

import cpat_model.constants as c

# [Post policy GDP]

def get_ec_sg_f(
        ec: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, s, f)
    # only 1 year at the time

    # Total energy consumption (TEC) without totals per fuel
    # Based on tables starting from 4625 (baseline) and 9615 (scenario)
    # only for FOSSIL_FUELS_AND_BIO

    ec_fuels_filtered = (
        ec[
            ec.index.get_level_values(c.FUEL_CODE).isin(FOSSIL_FUELS_AND_BIO)
        ]
    )

    # doing separate selects not to reset index
    # pow and oen are just selects
    ec_pow_oen = (
        ec_fuels_filtered[
            ec_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin([c.POW, c.OEN])
        ]
    )

    # in tra aggregation for ker we also add avi, jfu
    ec_tra = (
        ec_fuels_filtered[
            ec_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.TRA])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.TRA})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )
    ec_avi_jfu = (
        ec[
            ec.index.get_level_values(c.SECTOR_CODE).isin([c.AVI]) &
            ec.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
        ]
        .rename(index={c.AVI: c.TRA}, level=c.SECTOR_CODE)
        .rename(index={c.JFU: c.KER}, level=c.FUEL_CODE)
    )
    ec_tra = ec_tra.add(ec_avi_jfu, fill_value=0)

    ec_bld = (
        ec_fuels_filtered[
            ec_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.BLD])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.BLD})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    ec_ind = (
        ec_fuels_filtered[
            ec_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.IND])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.IND})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    ec_sg_f = pd.concat([ec_pow_oen, ec_tra, ec_bld, ec_ind]).sort_index()
    return ec_sg_f


def get_ec_f_totals(
        ec_sg_f: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, f)
    # only 1 year at the time

    # Total energy consumption (TEC), only totals per fuel
    # Based on tables starting from 4625 (baseline) and 9615 (scenario)

    ec_f_totals = (
        ec_sg_f
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    return ec_f_totals
