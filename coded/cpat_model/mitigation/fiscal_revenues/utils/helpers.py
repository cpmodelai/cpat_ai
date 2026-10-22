from typing import List

import pandas as pd

import cpat_model.constants as cnst

from cpat_model.mitigation.fiscal_revenues.utils.constants import CONV_MAPPING
from cpat_model.indicators.utils.constants import FOSSIL_FUELS_AND_BIO


# [Post policy GDP]

def get_r_taxes_by_fuel(
        ec_sg_f: pd.DataFrame,
        ec: pd.DataFrame,
        coa_nga: List[str],
        other_f: List[str],
        taxes: pd.DataFrame
        ) -> pd.DataFrame:

    ec_sg_no_oen = (
        ec_sg_f[
            ~ec_sg_f.index.get_level_values(cnst.SECTOR_CODE).isin([cnst.OEN])
        ]
    )

    ec_sg_coa_nga = (
        ec_sg_no_oen[
            ec_sg_no_oen.index.get_level_values(cnst.FUEL_CODE).isin(coa_nga)
        ]
        .rename(index={cnst.TRA: cnst.IND}, level=cnst.SECTOR_CODE)
        .groupby(level=cnst.ID_COL_NAMES)
        .sum()
    )

    # for f in [oop, gso, die, lpg, ker, bio] -> no oen
    # and for f == ker -> no ec(tra, jfu)
    ec_sg_other_f = (
        ec_sg_no_oen[
            ec_sg_no_oen.index.get_level_values(cnst.FUEL_CODE).isin(other_f)
        ]
    )
    # TODO extract ec_avi_jfu just once after having a structure
    # so we do not need to do it in every fnc
    ec_avi_jfu = (
        ec[
            ec.index.get_level_values(cnst.SECTOR_CODE).isin([cnst.AVI]) &
            ec.index.get_level_values(cnst.FUEL_CODE).isin([cnst.JFU])
        ]
        .rename(index={cnst.AVI: cnst.TRA}, level=cnst.SECTOR_CODE)
        .rename(index={cnst.JFU: cnst.KER}, level=cnst.FUEL_CODE)
    )
    ec_sg_other_f = (
        ec_sg_other_f
        .sub(ec_avi_jfu, fill_value=0)
        .groupby(level=[cnst.COUNTRY_CODE, cnst.FUEL_CODE])
        .sum()
    )

    # just 1 per sg is taken as for a given sg all subsectors have the same vat values
    taxes_filtered = (
        taxes[
            taxes.index.get_level_values(cnst.SECTOR_CODE).isin([cnst.POW, cnst.RES, cnst.MCH])
            & taxes.index.get_level_values(cnst.FUEL_CODE).isin(FOSSIL_FUELS_AND_BIO)
        ]
    )

    taxes_coa_nga = (
        taxes_filtered[
            taxes_filtered.index.get_level_values(cnst.FUEL_CODE).isin(coa_nga)
        ]
        .rename(index={cnst.RES: cnst.BLD}, level=cnst.SECTOR_CODE)
        .rename(index={cnst.MCH: cnst.IND}, level=cnst.SECTOR_CODE)
    )

    taxes_other_f = (
        taxes_filtered[
            taxes_filtered.index.get_level_values(cnst.SECTOR_CODE).isin([cnst.POW])
            & taxes_filtered.index.get_level_values(cnst.FUEL_CODE).isin(other_f)
        ]
        .groupby(level=[cnst.COUNTRY_CODE, cnst.FUEL_CODE])
        .sum()
    )

    r_taxes_by_fuel = (
        pd.concat([
            (
                (ec_sg_coa_nga * taxes_coa_nga)
                .groupby(level=[cnst.COUNTRY_CODE, cnst.FUEL_CODE])
                .sum()
            ),
            ec_sg_other_f * taxes_other_f
        ])
    )

    # we can do it because there is only 1 year at a time (1 column)
    r_taxes_by_fuel.iloc[:, 0] *= (
        r_taxes_by_fuel.index.get_level_values(cnst.FUEL_CODE)
        .map(CONV_MAPPING)
    )
    r_taxes_by_fuel.sort_index(inplace=True)

    return r_taxes_by_fuel
