import pandas as pd

import cpat_model.constants as cnst

from cpat_model.mitigation.fiscal_revenues.utils.helpers import get_r_taxes_by_fuel

# [Post policy GDP]

def get_r_existing_taxes(
        r_existing_taxes_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    Totals for:
    'Revenues from existing excises and other taxes, including consumer-side subsidies' (v361)
    CPAT Excel: baseline 6234, scenario 11224

    returns dims (c), t
    """

    r_existing_taxes = (
        r_existing_taxes_by_fuel
        .groupby(level=[cnst.COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_existing_taxes

def get_r_existing_taxes_by_fuel(
        ec_sg_f: pd.DataFrame, # (c, sg, f)
        ec: pd.DataFrame, # (c, s, f)
        fao: pd.DataFrame, # (c, s, f)
        cs: pd.DataFrame, # (c, s, f)
        xct: pd.DataFrame, # (c, s, f)
        xetsp: pd.DataFrame, # (c, s, f)
        is_eu_ets: bool # TODO: this should be country specific!, changed to ExistingETS.eu_ets
        ) -> pd.DataFrame: # (c, f)
    """
    'Revenues from existing excises and other taxes, including consumer-side subsidies' (v361)
    CPAT Excel: baseline 6225:6233, scenario 11215:11223

    returns dims (c, f), t
    """

    # TODO: elec after elasticity based power model
    coa_nga = [cnst.COA, cnst.NGA]
    other_f = [cnst.OOP, cnst.GSO, cnst.DIE, cnst.LPG, cnst.KER, cnst.BIO]

    existing_taxes = fao + cs + xct
    if not is_eu_ets:
        existing_taxes = existing_taxes + xetsp

    r_existing_taxes_by_fuel = get_r_taxes_by_fuel(
        ec_sg_f, ec, coa_nga, other_f, existing_taxes
    )

    return r_existing_taxes_by_fuel
