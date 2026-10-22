import pandas as pd

import cpat_model.constants as cnst

from cpat_model.mitigation.fiscal_revenues.utils.helpers import get_r_taxes_by_fuel

# [Post policy GDP]

def get_r_vat(
        r_vat_by_fuel: pd.DataFrame # (c, f)
        ) -> pd.DataFrame: # (c)
    """
    Totals for 'Revenues from VAT' (v361)
    CPAT Excel: baseline 6300, scenario 11290

    returns dims (c), t
    """

    r_vat = (
        r_vat_by_fuel
        .groupby(level=[cnst.COUNTRY_CODE])
        .sum(numeric_only=True)
    )

    return r_vat

def get_r_vat_by_fuel(
        ec_sg_f: pd.DataFrame, # (c, sg, f)
        ec: pd.DataFrame, # (c, s, f)
        vat: pd.DataFrame # (c, s, f)
        ) -> pd.DataFrame: # (c, f)
    """
    'Revenues from VAT' (v361)
    CPAT Excel: baseline 6291:6299, scenario 11281:11289

    returns dims (c, f), t
    """
    # TODO: elec after elasticity based power model
    coa_nga = [cnst.COA, cnst.NGA]
    other_f = [cnst.OOP, cnst.GSO, cnst.DIE, cnst.LPG, cnst.KER, cnst.BIO]

    r_vat_by_fuel = get_r_taxes_by_fuel(ec_sg_f, ec, coa_nga, other_f, vat)

    return r_vat_by_fuel
