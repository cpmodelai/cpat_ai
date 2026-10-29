"""Data steps: emission factors of the country (Excel-AI Inputs sheet). EQ-A7.1.

    co2_efs          CO2 factors by fuel and EF sector (tCO2/GJ; legacy Mitigation rows 980-1011): the factor of the
                     country (sheet EF_GHG, IIASA), else of its World Bank region, else of the world; some rows read
                     another fuel or sector (core/excel_ai/co2_ef_rows.csv); jet fuel the IEA factor; biomass 0
    co2_calibration  EFCalib: inventory energy CO2 of the year before the base year / scenario-1 energy CO2 with
                     uncalibrated factors (Excel-AI's stored BaselineCO2 'raw'), if the calibration is on
    nonco2_efs       other combustion factors (t/ktoe; GAINS, sheet EF_PM): country, else region, else world, else 0;
                     other energy use takes the largest factor of the fuel across the subsectors listed above it (issue I149)
"""
import numpy as np

from cpat_model.core import excel_ai_tables as xt
from cpat_model.data.database import to_float


def region(db, iso):
    """The country's World Bank region code, lower case (Excel-AI CtryReg)."""
    ca = db.table('countries_attributes')
    name = ca.loc[(ca['code'] == iso) & (ca['variable'] == 'Region'), 'value']
    ra = db.table('countries_region_attributes')
    ra = ra[ra['variable'] == 'Name (K)']
    code = ra.loc[ra['name'] == (name.iloc[0] if len(name) else ''), 'code']
    return code.iloc[0].lower() if len(code) else ''


def _pick(table, iso, reg, suffix):
    for code in (f'{iso.lower()}.mit.{suffix}', f'{reg}.mit.{suffix}', f'wld.mit.{suffix}'):
        if code in table:
            return table[code]
    return None


def co2_efs(db, iso, c):
    """{fuel|EF sector: tCO2/GJ} before calibration."""
    ef = db.table('ef_ghg')
    ef = dict(zip(ef['code'], to_float(ef['value'])))
    reg = region(db, iso)
    out = {}
    for r in xt.table('co2_ef_rows'):
        if r['source'] == 'IEA':
            out[r['key']] = c('EFJetIEA')
        elif r['source'] == 'IIASA':
            v = _pick(ef, iso, reg, f'ef.{r["source_sector"]}.{r["source_fuel"]}.co2')
            out[r['key']] = 0.0 if v is None or np.isnan(v) else v / c('KgPerT')
        else:
            out[r['key']] = 0.0
    return out


CALIBRATE = True        # Excel-AI Settings D27 'Yes*' (as legacy EFsAdjustmentAnnexI and NonAnnexI)


def co2_calibration(db, iso, settings, stored_raw):
    """EFCalib (Excel-AI Settings C29). stored_raw: scenario-1 energy CO2 with uncalibrated factors, base year."""
    if not CALIBRATE:
        return 1.0
    inv = db.table('ghg_inventory_energy')
    v = inv.loc[(inv['iso'] == iso) & (inv['year'] == str(settings.base_year - 1)) & (inv['gas'] == 'CO2'), 'value']
    if not len(v) or not stored_raw:
        return 1.0
    return float(v.iloc[0]) / stored_raw


def nonco2_efs(db, iso, c):
    """{sector.fuel.pollutant: (factor in the base year, final factor)} in t/ktoe."""
    ef = db.table('ef_local_pollutants')
    ef = {k: (a, b) for k, a, b in zip(ef['code'], to_float(ef['fe_in']), to_float(ef['fe_fin']))}
    reg = region(db, iso)
    rows = xt.table('nonco2_ef_rows')
    out = {}
    for r in rows:
        if r['sector'] == 'oen':
            continue
        v = _pick(ef, iso, reg, f'ef.{r["key"]}')
        a, b = (0.0, 0.0) if v is None else tuple(0.0 if np.isnan(x) else x for x in v)
        out[r['key']] = (a * c('EFtPerKtoe'), b * c('EFtPerKtoe'))
    for i, r in enumerate(rows):             # the rows of the pollutant above other energy use (not navigation, below)
        if r['sector'] == 'oen':
            same = [out[q['key']] for q in rows[:i]
                    if q['sector'] != 'oen' and q['fuel'] == r['fuel'] and q['pollutant'] == r['pollutant']]
            out[r['key']] = (max(x[0] for x in same), max(x[1] for x in same)) if same else (0.0, 0.0)
    return out
