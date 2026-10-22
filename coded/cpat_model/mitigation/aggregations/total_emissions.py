import pandas as pd

from cpat_model.indicators.utils.constants import SECTORS_AGG_TMP, FOSSIL_FUELS

import cpat_model.constants as c

# [Post policy GDP]

def get_em_sg_f(
        em: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, s, f)
    # only 1 year at the time

    # CO2 emissions by fuel and sector - CO2 emissions by fuel
    # Based on tables starting from 4705 (baseline) and 9695 (scenario)
    # Important: em already includes ef, so just this fnc just performs aggregation
    # Only for fossil fuels

    em_fuels_filtered = (
        em[
            em.index.get_level_values(c.FUEL_CODE).isin(FOSSIL_FUELS)
        ]
    )

    # doing separate selects not to reset index
    # pow and oen are just selects
    em_pow_oen = (
        em_fuels_filtered[
            em_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin([c.POW, c.OEN])
        ]
    )

    # in tra aggregation for ker we also add avi, jfu
    em_tra = (
        em_fuels_filtered[
            em_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.TRA])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.TRA})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )
    em_avi_jfu = (
        em[
            em.index.get_level_values(c.SECTOR_CODE).isin([c.AVI]) &
            em.index.get_level_values(c.FUEL_CODE).isin([c.JFU])
        ]
        .rename(index={c.AVI: c.TRA}, level=c.SECTOR_CODE)
        .rename(index={c.JFU: c.KER}, level=c.FUEL_CODE)
    )
    em_tra = em_tra.add(em_avi_jfu, fill_value=0)

    em_bld = (
        em_fuels_filtered[
            em_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.BLD])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.BLD})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    em_ind = (
        em_fuels_filtered[
            em_fuels_filtered.index.get_level_values(c.SECTOR_CODE).isin(SECTORS_AGG_TMP[c.IND])
        ]
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
        .assign(**{c.SECTOR_CODE: c.IND})
        .reset_index()
        .set_index(c.ID_COL_NAMES)
    )

    em_sg_f = pd.concat([em_pow_oen, em_tra, em_bld, em_ind]).sort_index()
    return em_sg_f


def get_em_f_totals(
        em_sg_f: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, f)
    # only 1 year at the time

    # CO2 emissions by fuel and sector - CO2 emissions by fuel
    # Based on tables starting from 4705 (baseline) and 9695 (scenario), only totals per fuel
    # Only for fossil fuels

    em_f_totals = (
        em_sg_f
        .groupby(level=[c.COUNTRY_CODE, c.FUEL_CODE])
        .sum(numeric_only=True)
    )

    return em_f_totals
