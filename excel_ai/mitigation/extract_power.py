"""v0.2.3: years to 2041 (the horizon of CPAT-AI-Mitigation-Prototype v0.4.7); otherwise as the previous version in Old/. 

v0.9.0 (Power_465, excel_ai/plans/Power_465.md): legacy_engineer_reference.csv adds sc_ind (row 3629), the consumer
tax/subsidy txo_res, txo_ind (rows 3606, 3635) and the over/under-estimated costs ores_res, ores_ind (rows 3607, 3636),
for the method test of the price chain on 465 (the other files are unchanged).

v0.8.5 (LD41, 2026-10-29): source moved from legacy 456 to 465. Rows up to 5666 are the same in both files; the
carbon-tax copy of the engineer model starts at row 9270 (456: 9285), offset 6316 (456: 6331; row map
legacy/bugfixes/data/rowmap_456_465.json). The 465 carbon-tax run is the 465 Dashboard's US$5 (2040), not US$50.

v0.3: adds planned retirement (legacy K5): power_tech.csv column planned_retirement (Yes/No: use the planned
retirement data instead of the retirement rate; legacy J3991 'Use Data?' = No for coal, the only type legacy offers it
for) and power_paths.csv rows pret|<type> (planned retirement, nameplate MW per year). The NoPropData legacy file
holds no planned-retirement data (legacy reads them from sheet Power, rows 1750-1878, empty for Egypt), so the rows
are 0 and the switches No: the feature is in place and Egypt results do not change until data are entered.

v0.2: adds the engineer-model inputs (plant data of A4, retirement, investment permissions and scale-up rates,
demand by subsector, balance shares, dispatch and investment parameters) and legacy_engineer_reference.csv (cached
inputs and results of the baseline and the carbon-tax run, for the method test).

Extract the power generation-cost and power-price inputs from the legacy workbook (Egypt, sheet Mitigation,
section 4 'Technoeconomic (engineer) power model', rows 2954-3927) to CSVs for CPAT-AI-Mitigation-Prototype.

Writes (data/):
  power_tech.csv     one row per generation type: capital cost, lifetime, efficiency, capacity factor, WACC,
                     decommissioning and transmission capex, fixed and variable O&M, fixed fuel cost (nuclear),
                     price fuel of section 2, VRE flag, EF of the power sector
  power_paths.csv    year paths 2022-2040: capex time factors, storage cost components, and the interim rows that
                     the engineer model will compute later (generation shares, investment shares, consumption)
  power_params.csv   scalars: transmission and distribution add-ons, pass-through, generation/consumption,
                     storage parameters, discounted lifetime of renewables
  legacy_power_reference.csv   cached legacy results and legacy inputs used only by the checks (method = legacy)

Every row is located by its table id and label (asserted), so a changed legacy file fails loudly.

    python extract_power.py
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'data', 'scripts'))
from legacy_csv import legacy_dir, save_to_tidy  # noqa: E402,F401  (data/Public01/tidy/ in the legacy CSV form)
import csv
import os

from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', '..', 'data', 'legacy', 'CPAT 1.0pre_465_Shell.xlsb')   # v0.8.5 (LD41): was 456
DATA = legacy_dir()
SRC_ISO = 'EGY'   # v0.3.3: country of the legacy run in the source file: the key (column country) of the rows written
YEARS = list(range(2022, 2042))   # v0.2.3: horizon to 2041 (legacy horizon)
YEARS_X = list(range(2021, 2042))          # legacy reference: 2021 (demand price lag) to 2041 (D9 window)
COL = {y: y - 2011 for y in YEARS_X}          # legacy Mitigation: 2022 in column L (index 11)
TECH = [('coa', 'Coal'), ('nga', 'Natural gas'), ('oop', 'Oil'), ('nuc', 'Nuclear'), ('wnd', 'Wind'),
        ('sol', 'Solar'), ('hyd', 'Hydro'), ('ore', 'Other renewables'), ('bio', 'Biomass')]
PRICE_CODE = {'coa': 'coa.pow', 'nga': 'nga.pow', 'oop': 'oop.all', 'bio': 'bio.all'}   # section 2 price fuels
VRE = {'wnd', 'sol', 'ore'}                 # carry the marginal storage cost (legacy C3)
VRE_SHARE = {'wnd', 'sol', 'ore'}           # count in the variable-renewable share (legacy rows 3851, 3907)
SRC = 'CPAT 1.0pre_465_NoPropData.xlsb, Mitigation row {}'


def read_rows():
    rows = {}
    with open_workbook(LEGACY) as wb, wb.get_sheet('Mitigation') as sh:
        for i, row in enumerate(sh.rows()):
            r = i + 1
            if 2950 <= r <= 4300 or 2430 <= r <= 2450 or 8745 <= r <= 8765 or 9265 <= r <= 10625:   # v0.8.5: 465 rows
                rows[r] = [c.v for c in row]
            if r > 10625:
                break
    return rows


def main():
    R = read_rows()

    def label(r, text, col=3):
        assert str(R[r][col]).strip().startswith(text), (r, R[r][col], text)

    def table(r0, tid):
        assert R[r0][2] == tid, (r0, R[r0][2], tid)

    def path(r):
        return [R[r][COL[y]] for y in YEARS]

    for r0, tid in ((2976, 'A2'), (3048, 'A8'), (3060, 'A9'), (3109, 'A14'), (3120, 'A15'), (3131, 'A16'),
                    (3168, 'B1'), (3180, 'B2'), (3202, 'B4'), (3338, 'D1'), (3349, 'D2'), (3451, 'E0'), (3036, 'A7')):
        table(r0, tid)
    # technology table (row offsets inside each legacy table follow TECH order). cax0 = capital cost at capex time
    # factor 1: the base-year capital cost (B2 column H) divided by the base-year factor (A7), so cax(t) = cax0 x tcf(t)
    tech = []
    a4 = {R[2999 + i][1]: 2999 + i for i in range(9)}                  # A4 rows: coa nga oil nuc wnd sol hyd ore bio
    for i, (f, _n) in enumerate(TECH):   # A4 capacity factor and efficiency used = A8, A9 (one column each kept)
        r4 = a4['oil' if f == 'oop' else f]
        assert abs(R[r4][22] - R[3049 + i][COL[2022]]) < 1e-12 and abs(R[r4][21] - R[3061 + i][COL[2022]]) < 1e-12, f
    for i, (f, name) in enumerate(TECH):
        label(4061 + i, name.split()[0] if f != 'oop' else 'Oil', col=3)
        label(4130 + i, name.split()[0] if f not in ('oop', 'nga') else ('Oil' if f == 'oop' else 'Natural'), col=3)
        for r in (2977, 3049, 3061, 3110, 3121, 3132, 3181, 3203, 3339, 3350, 3452, 3038, 3169):
            label(r + i, name.split()[0] if f != 'oop' else 'Oil')
        tech.append({
            'code': f, 'name': name,
            'cax0_usd_per_kw': R[3181 + i][7] / R[3038 + i][COL[2022]], 'life_years': R[2977 + i][19],
            'efficiency': R[3061 + i][COL[2022]], 'capacity_factor': R[3049 + i][COL[2022]],
            'wacc': R[3203 + i][7], 'dtc_usd_per_kw': R[3110 + i][COL[2022]],
            'tcx_usd_per_kw': R[3121 + i][COL[2022]], 'opf_usd_per_kwh': R[3132 + i][COL[2022]],
            'vop_usd_per_kwh': R[3339 + i][COL[2022]],
            'fuel_fixed_usd_per_kwh': R[3350 + i][COL[2022]] if f == 'nuc' else 0.0,
            'rns_usd_per_kwh': 0.0, 'price_code': PRICE_CODE.get(f, ''), 'vre': 1 if f in VRE else 0,
            'vre_share': 1 if f in VRE_SHARE else 0,
            'cap0_mw': R[a4['oil' if f == 'oop' else f]][24], 'gen0_mwy': R[a4['oil' if f == 'oop' else f]][12],
            'retire_rate': R[4011 + i][9], 'invest_permitted': R[4061 + i][6], 'invest_start': R[4061 + i][7],
            'scaleup_rate': R[4130 + i][6],
            'dispatch': 'cg' if f in ('coa', 'nga') else 'fixed',
            'planned_retirement': R[3991][9] if f == 'coa' else 'No',
            'source': SRC.format('2977-3350 (A2, A8, A9, A14-A16, B2, B4, D1, D2)')})
    with open(os.path.join(DATA, 'power_tech.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['country'] + list(tech[0]), lineterminator='\n')
        w.writeheader()
        w.writerows({'country': SRC_ISO, **t} for t in tech)
    # year paths
    label(3887, 'Capex battery'); label(3888, 'Capex interface'); label(3891, 'Opex per kwh storage')
    label(3900, 'Capex per kwh power produced'); label(3901, 'Opex Fix'); label(3902, 'Opex Var')
    label(3621, 'Residential Power Consumption'); label(3650, 'Industrial Power Consumption')
    paths = []
    label(3725, 'Road', col=3)
    with open(os.path.join(DATA, 'power_demand.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')   # v0.8.5: LF, as the files in the repository
        w.writerow(['country', 'subsector', 'name', 'ktoe_2022', 'legacy_row'])
        for j in range(15):
            w.writerow([SRC_ISO, R[3725 + j][2], R[3725 + j][3], R[3725 + j][11], 3725 + j])
    for i, (f, _n) in enumerate(TECH):
        paths.append([f'tcf|{f}', 'factor', 'capex time factor (A7)', 3038 + i] + path(3038 + i))
    paths += [['cbat', '$/kWh storage', 'battery capex (J2)', 3887] + path(3887),
              ['cint', '$/kW interface', 'battery interface capex (J2)', 3888] + path(3888),
              ['obat', '$/kWh storage/y', 'battery opex (J2)', 3891] + path(3891),
              ['cel', '$/kWh produced', 'electrolyser cost per marginal unit: capex + fixed + variable opex (J2)',
               '3900-3902'] + [R[3900][COL[y]] + R[3901][COL[y]] + R[3902][COL[y]] for y in YEARS],
              ['incf', 'factor', 'income-dependent factor on GDP elasticities (macro block)', 2433] + path(2433),
              ['shock', 'share', 'exogenous shock on energy consumption (legacy calibration, 2023-2024)', 2439]
              + path(2439)]
    label(3991, 'Do Not Use Planned Retirement'); label(3992, 'Planned Retirement Coal')
    assert R[3991][9] == 'No', R[3991][9]
    for f, _n in TECH:             # planned retirement (MW nameplate): no data in the legacy file (sheet Power empty)
        paths.append([f'pret|{f}', 'MW', 'planned retirement, nameplate (K5; used if planned_retirement = Yes)',
                      3992 if f == 'coa' else ''] + [0.0] * len(YEARS))
    label(2433, 'Discount factor (proportion'); label(2439, 'Exogenous shock'); label(2446, 'Post-policy GDP')
    with open(os.path.join(DATA, 'power_paths.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')   # v0.8.5: LF, as the files in the repository
        w.writerow(['country', 'key', 'unit', 'description', 'legacy_row'] + YEARS)
        w.writerows([SRC_ISO] + p for p in paths)
    # scalars
    label(3599, 'Transmission'); label(3628, 'Transmission'); label(3596, 'Passthrough')
    label(3723, 'Generation/Consumption'); label(3883, 'Discounted Lifetime of renewables')
    for r, t in ((3871, 'Percent allocation of ST'), (3873, 'Marginal hours ST'), (3874, 'kwh storage to kw'),
                 (3877, 'Starting point of long term')):
        label(r, t)
    params = [('tmc|res', R[3599][COL[2022]], '$/kWh', 'transmission and distribution, residential (G1)', 3599),
              ('tmc|ind', R[3628][COL[2022]], '$/kWh', 'transmission and distribution, industrial (G2)', 3628),
              ('pass', R[3596][COL[2022]], 'share', 'pass-through of supply-cost changes to end users (G1)', 3596),
              ('gen_per_cons', R[3723][8], 'ratio', 'generation / final consumption (H2, base year)', 3723),
              ('dlf_ren', R[3883][COL[2022]], 'years', 'discounted lifetime of renewables (J2)', 3883),
              ('st_alloc', R[3871][4], 'share', 'allocation of short-term storage cost to VRE (J1)', 3871),
              ('st_marg_hours', R[3873][4], 'hours', 'marginal hours of short-term storage per unit VRE (J1)', 3873),
              ('st_ratio', R[3874][4], 'hours', 'kWh storage per kW interface (J1)', 3874),
              ('lt_start', R[3877][4], 'share', 'VRE share where long-term storage starts (J1)', 3877),
              ('lt_alloc', R[3876][4], 'share', 'allocation of long-term storage cost to VRE (J1)', 3876),
              ('sh_nxp', R[3719][8], 'share', 'net exports / final demand, base year (H2)', 3719),
              ('sh_tsd', R[3720][8], 'share', 'transmission and statistical differences / final demand (H2)', 3720),
              ('sh_eou', R[3721][8], 'share', 'energy industry own use / final demand (H2)', 3721),
              ('sh_add', R[3722][8], 'share', 'additional statistical difference / final demand (H2)', 3722),
              ('extra_eff', (R[3719] + [None] * 13)[12] or 0.0, 'share',     # v0.8.5: cell gone in 465 (456: M3719 = 0)
               'additional efficiency improvement of power demand (H2; not in legacy 465: 0)', 3719),
              ('maxcf_cg', R[3783][11], 'share', 'maximum capacity factor of coal and gas (I2)', 3783),
              ('k_dispatch', R[3720][12], 'factor', 'logit K parameter, dispatch (H2)', 3720),
              ('k_invest', R[3721][12], 'factor', 'logit K parameter, investment (H2)', 3721),
              ('min_cost', R[3463][10], '$/kWh', 'minimum cost in the logits (E1 column K)', 3463),
              ('early_max', R[3975][9], 'share', 'maximum early coal retirement, share of coal effective capacity (K4)', 3975),
              ('early_factor', R[3993][5], 'share', 'factor on cost-based early coal retirement (K5)', 3993),
              ('ktoe_gwh', 11.63, 'GWh/ktoe', 'GWh per ktoe', '')]
    with open(os.path.join(DATA, 'power_params.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')   # v0.8.5: LF, as the files in the repository
        w.writerow(['country', 'key', 'value', 'unit', 'description', 'legacy_row'])
        w.writerows([SRC_ISO] + list(p) for p in params)
    # legacy results and inputs for the method test
    ref = []
    blocks = {'B2 caxav': 3181, 'B6 stoav': 3225, 'B8 fix': 3247, 'C3 msc': 3282, 'C7 lfx': 3326,
              'D4 vbc': 3374, 'E3 gnc': 3486, 'A13 cax': 3099}
    for name, r0 in blocks.items():
        for i, (f, _n) in enumerate(TECH):
            ref.append([f'{name}|{f}', r0 + i] + path(r0 + i))
    for name, r in (('E3 gncav', 3495), ('J msc_st', 3910), ('J msc_lt', 3911), ('J vre', 3907),
                    ('J cph', 3905), ('G1 sc', 3600), ('G2 sc', 3629), ('G1 rppre', 3613), ('G2 rppre', 3642),
                    ('G1 vat', 3611), ('G2 vat', 3640), ('A18 coa', 3155), ('A18 nga', 3156), ('A18 oop', 3157),
                    ('A18 bio', 3163)):
        ref.append([name, r] + path(r))
    for name, r in (('E0 gns|' + f, 3452 + i) for i, (f, _n) in enumerate(TECH)):
        ref.append([name, r] + path(r))
    for name, r in (('B1 phi|' + f, 3169 + i) for i, (f, _n) in enumerate(TECH)):
        ref.append([name, r] + path(r))
    with open(os.path.join(DATA, 'legacy_power_reference.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')   # v0.8.5: LF, as the files in the repository
        w.writerow(['key', 'legacy_row'] + YEARS)
        w.writerows(ref)
    # engineer model: cached inputs and results of the baseline and the carbon-tax run (rows + 6316; 456: + 6331)
    eng = []
    off = {'base': 0, 'ctax': 9270 - 2954}             # v0.8.5: 465 row 9270 (456: 9285)

    assert str(R[9270][1]).startswith("Technoeconomic") and "Carbon tax" in str(R[9270][1]), R[9270][:3]
    single = {'gdp': 2446, 'inc': 2433, 'shock': 2439, 'cpf': 3683, 'rp_res': 3617, 'rp_ind': 3646, 'rppre_res': 3613,
              'rppre_ind': 3642, 'vat_res': 3611, 'vat_ind': 3640, 'req': 3752, 'vre': 3907, 'msc': 3912,
              'gncav': 3495, 'ccpav': 3395, 'need': 4028, 'early': 3993, 'sc_res': 3600, 'demtot': 3741,
              # v0.9.0 (Power_465): G1/G2 consumer tax/subsidy (input) and over/under-estimated costs (result)
              'sc_ind': 3629, 'txo_res': 3606, 'txo_ind': 3635, 'ores_res': 3607, 'ores_ind': 3636}
    per_tech = {'vbc': 3374, 'd5': 3385, 'd6': 3412, 'tvc': 3423, 'cfp': 3049, 'df': 3012, 'cap': 3932, 'gen': 3804,
                'shr': 3840, 'pe': 3855, 'ret': 3994, 'reteff': 4011, 'pni': 4085, 'first': 4143, 'second': 4238,
                'nei': 4251, 'nim': 4264, 'usd': 4276, 'phi': 3169, 'tic': 4035, 'lfx': 3326, 'caxav': 3181,
                'stoav': 3225, 'gnc': 3486, 'maxinv': 4130}
    for run, o in off.items():
        for k, r in single.items():
            eng.append([k, run, r + o] + [R[r + o][COL[y]] for y in YEARS_X])
        for k, r in per_tech.items():
            for i, (f, _n) in enumerate(TECH):
                eng.append([f'{k}|{f}', run, r + o + i] + [R[r + o + i][COL[y]] for y in YEARS_X])
        for j in range(15):
            eng.append([f'dem|{R[3725 + j][2]}', run, 3725 + o + j] + [R[3725 + o + j][COL[y]] for y in YEARS_X])
    with open(os.path.join(DATA, 'legacy_engineer_reference.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')   # v0.8.5: LF, as the files in the repository
        w.writerow(['key', 'run', 'legacy_row'] + YEARS_X)
        w.writerows(eng)
    print(f'wrote power_demand.csv, legacy_engineer_reference.csv ({len(eng)})')
    print(f'wrote power_tech.csv ({len(tech)}), power_paths.csv ({len(paths)}), power_params.csv ({len(params)}), '
          f'legacy_power_reference.csv ({len(ref)})')


if __name__ == '__main__':
    main()
