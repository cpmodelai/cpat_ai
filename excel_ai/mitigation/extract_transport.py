"""v3.5 (phase 1 of Transport_Plan.md): data of the engineer road transport model.

Source: legacy CPAT `excel_ai/legacy/workbooks/CPAT 1.0pre_465_NoPropData.xlsb` (read-only), cached values read
with pyxlsb. Layout and formulas are documented in Transport_Legacy_Survey.md (formulas were read from the xlsx
conversion with the defined names restored; this script needs the xlsb only).

Writes (data/):
  transport_data.csv          sheet Transport1: all countries, numeric variables, 2022-2025 (iso, country, variable)
  transport_data_sources.csv  sheet Transport1: the '... - source' text columns, same layout
  vehicle_prices.csv          sheet Transport2: vehicle purchase prices, all countries, 2022-2040
  range_anxiety.csv           sheet Transport3 rows 5-226: stored range-anxiety calibration per country ($/vehicle;
                              passenger H, freight N, 2-3 wheeler T) and the 2025 EV sales shares it was fitted to
  transport_params.csv        global parameters and policy defaults (Dashboard rows 61-98 and 540-559 via the
                              Mitigation side tables rows 4303-4332), hardcoded literals of the formulas, and the
                              methodology-note alternatives (use = note, not used by default)
  transport_paths.csv         global year paths 2022-2041: BEV fuel economy of new vehicles ('Manual inputs' rows
                              375-377), BEV fuel economy light/freight/2-3 wheeler (Mitigation rows 2051, 2095, 2122),
                              charging-station cost per port (row 2170)
  legacy_transport_reference.csv
                              cached legacy values of both scenario blocks (run base: rows 4334-5378; run pol: the
                              policy copy at +6316; 456: +6331), the key-input block rows 2017-2171 (shared), side-table scalars
                              (calibration factors etc.), and the legacy inputs the engineer model takes from the rest
                              of Mitigation (keys in|...), for transport_model_ref.legacy_inputs/legacy_test

v8.5 (LD41, 2026-10-29): source moved from legacy 456 to 465. Rows up to 5666 are the same in both files; the policy
block moved up by 15 rows (OFF 6331 -> 6316; row map legacy/bugfixes/data/rowmap_456_465.json). The 465 policy run is
the 465 Dashboard's carbon tax of US$5 (2040), not US$50.

Every year row is checked against its legacy label (column D) so a changed legacy file fails loudly.

    python extract_transport.py
"""
import csv
import os
import re

from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', 'legacy', 'workbooks', 'CPAT 1.0pre_465_NoPropData.xlsb')   # v8.5 (LD41): was 456
DATA = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
SRC = 'CPAT 1.0pre_465_NoPropData.xlsb'
YEARS = list(range(2022, 2042))              # legacy Mitigation L (2022) .. AE (2041)
YEARS_X = list(range(2021, 2042))            # with K (2021) for the lagged inputs
COL = {y: y - 2011 for y in YEARS_X}         # 0-based column index: K = 10, L = 11
OFF = 6316                                   # policy scenario block = baseline block + 6316 rows (465; 456: 6331)
SEC = (4334, 5378)                           # engineer section 5 rows tested (baseline numbering)
KEYB = (2017, 2171)                          # key inputs 15 (shared by both scenarios)
SRC_ISO = None                               # country of the legacy run: Dashboard!D644 (_Country_code), set in main


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def cell(ref):
    m = re.match(r'([A-Z]+)(\d+)$', ref)
    return int(m.group(2)), col_index(m.group(1))


def load(wb, sheet, last=None):
    out = {}
    with wb.get_sheet(sheet) as sh:
        for row in sh.rows(sparse=True):
            if not row:
                continue
            r = row[0].r + 1
            if last and r > last:
                break
            for c in row:
                if c.v is not None and c.v != '':
                    out[(r, c.c)] = c.v
    return out


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def write(name, header, rows):
    with open(os.path.join(DATA, name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(header)
        w.writerows(rows)
    print(f'wrote {name} ({len(rows)} rows)')


# ---------------------------------------------------------------- parameters: (key, legacy cell, unit, description)
# Policy and parameter side table of Mitigation section 5 (baseline block; the policy block holds the same values).
# The Dashboard cell each one reads is given in the description (Mitigation side cell = Dashboard cell).
SIDE = [
    # feebate (Dashboard rows 63-67, passenger G / freight L / 2-3 wheeler Q)
    ('fb_year|{c}', ('J4304', 'K4304', 'L4304'), 'year', 'feebate: year of introduction (Dashboard {d}63)'),
    ('fb_rate|{c}', ('J4305', 'K4305', 'L4305'), 'USD/tCO2', 'feebate: price level (Dashboard {d}64)'),
    ('fb_pivot_type|{c}', ('J4306', 'K4306', 'L4306'), 'option', 'feebate: pivot type Average/Manual (Dashboard {d}65)'),
    ('fb_pivot|{c}', ('J4307', 'K4307', 'L4307'), 'gCO2/km', 'feebate: manual pivot point (Dashboard {d}66)'),
    ('fb_pivot_chg|{c}', ('J4308', 'K4308', 'L4308'), 'gCO2/km', 'feebate: annual decline of manual pivot (Dashboard {d}67)'),
    # distance tax (Dashboard rows 73-76)
    ('dt_year|{c}', ('P4304', 'Q4304', 'R4304'), 'year', 'distance tax: year of introduction (Dashboard {d}73)'),
    ('dt_start|{c}', ('P4305', 'Q4305', 'R4305'), 'USD/km', 'distance tax: amount in first year (Dashboard {d}74)'),
    ('dt_target_year|{c}', ('P4306', 'Q4306', 'R4306'), 'year', 'distance tax: target year (Dashboard {d}75)'),
    ('dt_target|{c}', ('P4307', 'Q4307', 'R4307'), 'USD/km', 'distance tax: amount in target year (Dashboard {d}76)'),
    # VAT and customs (Dashboard rows 81, 86); the rates themselves are country data (see country_side below)
    ('vat_year|{c}', ('V4307', None, 'X4307'), 'year', 'year of policy VAT change on BEVs (Dashboard {d}81)'),
    ('cust_year|{c}', ('V4311', 'W4311', 'X4311'), 'year', 'year of policy customs change on BEVs (Dashboard {d}86)'),
    # EV purchase subsidy (Dashboard rows 69-71)
    ('sub_year|{c}', ('AB4304', 'AC4304', 'AD4304'), 'year', 'EV subsidy: year of introduction (Dashboard {d}69)'),
    ('sub_amount|{c}', ('AB4305', 'AC4305', 'AD4305'), 'USD/vehicle', 'EV subsidy: amount (Dashboard {d}70)'),
    ('sub_chg|{c}', ('AB4306', 'AC4306', 'AD4306'), 'USD/vehicle', 'EV subsidy: annual change (Dashboard {d}71)'),
    # ad-valorem purchase tax (Dashboard rows 89-93)
    ('adv_ice_base|{c}', ('J4315', 'K4315', 'L4315'), 'share', 'ad-valorem tax on ICEVs, baseline (Dashboard {d}89)'),
    ('adv_bev_base|{c}', ('J4316', 'K4316', 'L4316'), 'share', 'ad-valorem tax on BEVs, baseline (Dashboard {d}90)'),
    ('adv_ice_pol|{c}', ('J4317', 'K4317', 'L4317'), 'share', 'ad-valorem tax on ICEVs, policy (Dashboard {d}91)'),
    ('adv_bev_pol|{c}', ('J4318', 'K4318', 'L4318'), 'share', 'ad-valorem tax on BEVs, policy (Dashboard {d}92)'),
    ('adv_year|{c}', ('J4319', 'K4319', 'L4319'), 'year', 'year of policy ad-valorem tax change (Dashboard {d}93)'),
    # vehicle parameters (Dashboard rows 542-547, 548-549 R/V, 551-553 L)
    ('own_years|{c}', ('J4322', None, None), 'years', 'years of ownership of a new vehicle (Dashboard {d}542)'),
    ('life|{c}', ('J4324', 'K4324', 'L4324'), 'years', 'useful life (Dashboard {d}543)'),
    ('dep1|{c}', ('J4325', 'K4325', 'L4325'), 'share', 'depreciation in first year (Dashboard {d}544)'),
    ('ins|{c}', ('J4326', 'K4326', 'L4326'), 'share/y', 'insurance, share of value (Dashboard {d}545)'),
    ('maint_ice|{c}', ('J4327', 'K4327', 'L4327'), 'USD/km', 'ICEV maintenance (Dashboard {d}546)'),
    ('maint_ev|{c}', ('J4328', 'K4328', 'L4328'), 'USD/km', 'EV maintenance (Dashboard {d}547 = ICEV x 2/3)'),
    ('inc_el_vkt|{c}', ('J4330', 'K4330', 'L4330'), 'elasticity',
     'income elasticity of distance driven (Dashboard V548 passenger and freight, V549 2-3 wheeler)'),
    ('fe_gap|{c}', ('J4331', 'K4331', 'L4331'), 'share', 'new versus stock-average fuel economy (Dashboard V542)'),
    ('k|{c}', ('J4332', 'K4332', 'L4332'), 'factor', 'logit k-parameter of the EV choice (Dashboard L551-L553)'),
    # ownership (Dashboard R543-V547, H554-L556)
    ('own_adj|{c}', ('T4322', 'U4322', 'V4322'), 'share/y', 'partial adjustment speed of ownership (Dashboard V543)'),
    ('own_gomp_b|{c}', ('T4323', 'U4323', None), 'per 1000 USD', 'Gompertz income coefficient (Dashboard V544)'),
    ('own_max_growth|{c}', ('T4327', 'U4327', 'V4327'), 'share/y', 'ownership: maximum annual growth (Dashboard L554)'),
    ('own_max_decline|{c}', ('T4328', 'U4328', 'V4328'), 'share/y',
     'ownership: maximum annual decrease (Dashboard L555; 2-3 wheeler L556)'),
]
SIDE_SINGLE = [
    ('vkt_disc_gap', 'U4324', 'share', 'difference between discounted and average VKT (Dashboard V545; unused, B15)'),
    ('fre_vkt_min', 'U4325', 'km', 'minimum VKT, freight, TCO (Dashboard V546)'),
    ('fre_vkt_max', 'U4326', 'km', 'maximum VKT, freight, TCO (Dashboard V547)'),
    ('ch_el_stock', 'P4322', 'elasticity', 'elasticity of charging stations to the BEV stock (Dashboard G551)'),
    ('ch_cost_max', 'P4323', 'USD/kWh', 'maximum charging cost mark-up (Dashboard G552)'),
    ('ch_cost_min', 'P4324', 'USD/kWh', 'minimum charging cost mark-up (Dashboard G553)'),
    ('ch_sat', 'P4325', 'share', 'EV fleet share where the mark-up reaches its minimum (Dashboard G554)'),
    ('ch_public', 'P4326', 'share', 'share of public charging (Dashboard G555)'),
    ('ra_el_stations', 'P4327', 'elasticity', 'elasticity of range anxiety to charging stations (Dashboard G556)'),
    ('ch_el_cost', 'P4328', 'elasticity', 'elasticity of charging stations to their cost (Dashboard G557)'),
    # charging-station subsidy: the formula (row 4343) reads the cells in this order; the Dashboard labels of rows
    # 95-98 do not match it (B10): G95 is used as the start level, G96 as the target level, G97 as the start year and
    # G98 as the target year
    ('cs_start_level', 'P4315', 'share', 'charging-station subsidy, start level (Dashboard G95, labelled "start year")'),
    ('cs_target_level', 'P4316', 'share', 'charging-station subsidy, target level (Dashboard G96, labelled "start level")'),
    ('cs_start_year', 'P4317', 'year', 'charging-station subsidy, start year (Dashboard G97, labelled "target year")'),
    ('cs_target_year', 'P4318', 'year', 'charging-station subsidy, target year (Dashboard G98, labelled "target level")'),
    ('disc_max', 'Z4322', 'share', 'consumer discount rate at low income (Dashboard Q552)'),
    ('disc_inc_low', 'Z4323', 'USD/cap', 'income threshold, low income (Dashboard Q553)'),
    ('disc_min', 'Z4324', 'share', 'consumer discount rate at high income (Dashboard Q554)'),
    ('disc_inc_high', 'Z4325', 'USD/cap', 'income threshold, high income (Dashboard Q555)'),
    ('own_price_el', 'T4329', 'elasticity',
     'ICE fuel split: own-TCO elasticity, hardcoded =AVERAGE(-1.72,-1.27,-1.08,-0.99) (T4329:V4329)'),
    ('cross_price_el', 'T4330', 'elasticity',
     'ICE fuel split: cross-TCO elasticity, hardcoded =AVERAGE(0.71,0.43,0.51,0.64) (T4330:V4330)'),
]
DASH = [   # (key, Dashboard cell, unit, description)
    ('tr_model', 'G61', 'option', 'TrModel default (Engineer/Elasticity); MTInputs F340 = Dashboard G61'),
    ('ra_source', 'L61', 'option', 'RngAnxietySource: Solver = Transport3 per country, Dashboard = values below'),
    ('ra_dash|pass', 'G548', 'USD/vehicle', 'range anxiety, start value if the source is Dashboard (PassAnxiety)'),
    ('ra_dash|fre', 'L548', 'USD/vehicle', 'range anxiety, start value if the source is Dashboard (FreightAnxiety)'),
    ('ra_dash|cyc', 'Q548', 'USD/vehicle', 'range anxiety, start value if the source is Dashboard (MotorAnxiety)'),
    ('ra_decline|pass', 'G549', 'share/y', 'range anxiety, annual decline (PassAnxietyDecline)'),
    ('ra_decline|fre', 'L549', 'share/y', 'range anxiety, annual decline (FreightAnxietyDecline)'),
    ('ra_decline|cyc', 'Q549', 'share/y', 'range anxiety, annual decline (MotorAnxietyDecline)'),
    ('vkt_new_price', 'Q551', 'option', 'TCO distance of new vehicles responds to prices (Yes/No; rows 4465-4505)'),
    ('recon_ele', 'Q556', 'option', 'reconcile road electricity with the energy balance (Yes/No; E5331)'),
    ('cyc_peak_inc', 'V551', 'USD/cap', '2-3 wheeler ownership hump: peak income H2169'),
    ('cyc_scale', 'V552', 'factor', '2-3 wheeler ownership hump: scaling factor I2169'),
    ('fre_inc_target', 'V553', 'USD/cap', 'income where the freight/passenger ownership ratio reaches its target H2168'),
    ('fre_share_target', 'V554', 'share', 'target freight/passenger ownership ratio I2168'),
    ('purch_gdp', 'L557', 'share of GDP', 'vehicle purchases, actual data (unused by the formulas)'),
    ('purch_year', 'L558', 'year', 'vehicle purchases, actual data year (unused)'),
    ('purch_anchor', 'L559', 'option', 'anchor vehicle purchases (unused)'),
]
LITERALS = [  # (key, value, unit, description, legacy cells)
    ('gomp_a', -5.897, 'factor', 'Gompertz constant of ownership demand exp(a*exp(b*GDPpc/1000))', 'L4786, H4787, L4902, H4903'),
    ('gas_l_per_gj', 26.0, 'l/GJ', 'natural gas $/GJ to $/liter-equivalent (prices /26; EF per GJ /26)',
     'L4370, L4412, G4378, G4421'),
    ('phev_l_per_kwh', 9.0, 'kWh/l', 'PHEV: kWh x 9 = liter gasoline equivalent in the PHEV fuel price', 'L4371'),
    ('ins_factor', 0.5, 'factor', 'factor 0.5 on the insurance annuity', 'L4541, L4573, L4600, L4615, L4648, L4672, L4706, L4727'),
    ('station_life', 15.0, 'years', 'charging-station life in "stations added" (memo row)', 'M4348'),
    ('bev_vkt_cap|pass', 1.2, 'factor', 'cap on BEV/ICEV distance ratio, passenger (TCO distance)', 'H2056'),
    ('bev_vkt_cap|fre', 1.0, 'factor', 'cap on BEV/ICEV distance ratio, freight', 'H2114'),
    ('bev_vkt_cap|cyc', 1.0, 'factor', 'cap on BEV/ICEV distance ratio, 2-3 wheeler', 'H2136'),
    ('vat_pol_factor', 1.0, 'factor', 'policy VAT on BEVs = baseline x factor (formula literal *1)', 'Dashboard G80, Q80'),
    ('cust_pol_factor', 1.0, 'factor', 'policy customs on BEVs = baseline x factor (formula literal *1)',
     'Dashboard G85, L85, Q85'),
    ('customs_year', 2024, 'year', 'data year of the customs rates (Dashboard G83:Q84 = Mitigation N2157:N2162)', 'Dashboard G83:Q84'),
    ('import_year', 2022, 'year', 'data year of the import shares (Dashboard G87 = L2163, L87 = L2164; 2-3 wheeler = passenger)',
     'Dashboard G87:Q87'),
    ('own_calib_year', 2024, 'year', 'year of the ownership calibration actual/expected (B3: column N hardcoded)',
     'H4787:I4787, H4903:I4903, $N2168, J2169'),
    ('bus_ele_year', 2024, 'year', 'year of the EV stock share used for bus electricity (N2064)', 'L2143'),
]
NOTE = [   # methodology note (Transportation_methodology.docx) values, not used by default
    ('note|disc_max', 0.30, 'share', 'discount rate, low-income countries (note: 30%; legacy 15%)'),
    ('note|disc_min', 0.10, 'share', 'discount rate, high-income countries (note: 10%; legacy 5%)'),
    ('note|inc_el_vkt', 0.05, 'elasticity', 'income elasticity of distance driven (note: 0.05; legacy 0.1, 2-3 wheeler -0.4)'),
    ('note|el_vkt_ldv', -0.3, 'elasticity', 'driving elasticity, LDV and 2-3 wheelers (note: -0.3; legacy _el_dem_gso_rod -0.4)'),
    ('note|el_vkt_hdv', -0.2, 'elasticity', 'driving elasticity, HDV (note: -0.2; legacy _el_dem_die_rod -0.3)'),
    ('note|maint_ev_factor', 1 / 3, 'factor', 'EV maintenance = ICEV x factor (note: 1/3; legacy 2/3)'),
    ('note|bev_vkt_cap|pass', 1.0, 'factor', 'BEV and ICEV distance identical in the TCO (note; legacy cap 1.2)'),
    ('note|ch_cost_max', 0.10, 'USD/kWh', 'maximum charging mark-up (note: 0.10; legacy 0.3)'),
    ('note|maint_wages', '', 'text', 'maintenance cost varies with wages (note); legacy fixed USD/km'),
    ('note|icev_price_income', '', 'text', 'ICEV price rises with income (note); legacy Transport2 path'),
]
CLS = ('pass', 'fre', 'cyc')
DCOL = {'pass': 'G', 'fre': 'L', 'cyc': 'Q'}

# legacy inputs from the rest of Mitigation (per run: row + OFF in the policy block)
IN_RUN = [   # (key, row, label start in column D)
    ('rp_gso', 2589, 'Retail price'), ('sp_gso', 2590, 'Pre-tax prices'), ('vatr_gso', 2594, 'VAT rate'),
    ('txo_gso', 2596, 'Excise and other taxes'), ('rp_die', 2612, 'Retail price'), ('vat_die', 2618, 'VAT payment'),
    ('rp_lpg', 2635, 'Retail price'), ('vat_lpg', 2641, 'VAT payment'), ('rp_nga_res', 2543, 'Retail price'),
    ('rp_nga_ind', 2566, 'Retail price'), ('vat_nga_ind', 2572, 'VAT payment'),
    ('pp_res', 3617, 'Residential power price'), ('pp_ind', 3646, 'Industrial power price'),
    ('gdp_growth', 2446, 'Post-policy GDP growth'), ('row2455', 2455, '- in which: producer-side subsidies'),
    ('cprice', 2375, None), ('fb_cov', 2404, 'Road')]
IN_SHARED = [('pop', 428, 'Population'), ('gdppc', 444, 'GDP real per capita'),
             # section 2 price block (not scenario-specific; the key-input rows 2054-2135 use 2022-2025)
             ('rp0_gso', 797, 'Retail price'), ('rp0_ele_res', 789, 'Retail price'), ('rp0_die', 802, 'Retail price'),
             ('vatr0_die', 805, 'VAT rate'), ('rp0_ele_ind', 793, 'Retail price')]
IN_CELLS = [   # (key, cell, expected label cell or None, description)
    ('rp0_ele_res_2021', 'K789', 'mit.rp.ecy.res', 'residential electricity retail price 2021 (row 2055)'),
    ('vat_veh', 'N726', None, 'VAT rate 2024 (VAT_WEO), the VAT on vehicles (Dashboard G78/Q78)'),
    ('el_dem_gso', 'K330', None, '_el_dem_gso_rod'), ('el_dem_die', 'K331', None, '_el_dem_die_rod'),
    ('el_eff_gso', 'K339', None, '_el_eff_gso_rod'), ('el_eff_die', 'K340', None, '_el_eff_die_rod'),
    ('aei_oil', 'K373', None, '_eff_imp_oil_rod'),
    ('l_ktoe|gso', 'O949', None, '_conv_ktoe_liter_gso'), ('l_ktoe|die', 'O950', None, '_conv_ktoe_liter_die'),
    ('l_ktoe|lpg', 'O951', None, '_conv_ktoe_liter_lpg'), ('l_ktoe|nga', 'O948', None, '_conv_ktoe_liter_nga (= gasoline)'),
    ('gwh_ktoe', 'E1033', None, '_conv_ktoe_to_gwh'),
    ('ef|gso', 'O989', None, '_ef_co2_gso_rod_lit (tCO2/l)'),
    ('ef_name|die', 'O1004', None, '_ef_co2_ker_ind_lit = diesel, industry (used by legacy for diesel, B7)'),
    ('ef_name|lpg', 'O1005', None, '_ef_co2_jet_avi_lit = LPG, industry (used by legacy for LPG, B7)'),
    ('ef_name|nga_gj', 'O995', None, '_ef_co2_die_pow_lit = natural gas, residential, tCO2/GJ (used for CNG/LNG, B7)'),
    ('ef|die', 'O990', None, 'diesel, road (tCO2/l)'), ('ef|lpg', 'O991', None, 'LPG, road (tCO2/l)'),
    ('ef|nga_gj', 'O988', None, 'natural gas, road (tCO2/GJ)'),
    ('eb|gso', 'G587', None, 'energy balance base year, road gasoline (ktoe)'),
    ('eb|die', 'G588', None, 'road diesel'), ('eb|lpg', 'G590', None, 'road LPG'), ('eb|nga', 'G585', None, 'road gas'),
    ('eb|bgs', 'G598', None, 'road biogasoline'), ('eb|bdi', 'G599', None, 'road biodiesel'),
    ('eb|ele', 'G583', None, 'road electricity'),
]
SCALARS = ['H4787', 'I4787', 'J4787', 'H4903', 'I4903', 'J4903', 'G5177', 'G5231', 'G5273',
           'G4375', 'G4376', 'G4377', 'G4378', 'G4419', 'G4420', 'G4421', 'G4441', 'K4329',
           'E5325', 'E5326', 'E5327', 'E5328', 'E5331', 'I5325', 'I5326', 'I5327', 'I5328', 'I5331',
           'J5325', 'J5326', 'J5327', 'J5328', 'J5331'] + \
          [f'{c}{r}' for r in range(5170, 5174) for c in 'LMNOPQRSTUVW'] + \
          [f'{c}4304' for c in ('V', 'X')] + [f'{c}{r}' for r in range(4305, 4313) for c in 'VWX'] + \
          ['E5306', 'E5307', 'E5308', 'E5309', 'E5310', 'E5311', 'E5312', 'E5313', 'E5314']
SCALARS_KEYB = ['J2169', 'H2168', 'I2168', 'H2169', 'I2169', 'E2089', 'E2146', 'E2147', 'C2017', 'C2020',
                'C2024', 'C2028'] + [f'{c}{r}' for r in range(2017, 2032) for c in 'LMN']


def main():
    global SRC_ISO
    with open_workbook(LEGACY) as wb:
        M = load(wb, 'Mitigation', last=SEC[1] + OFF + 2)
        D = load(wb, 'Dashboard', last=700)
        T1 = load(wb, 'Transport1')
        T2 = load(wb, 'Transport2')
        T3 = load(wb, 'Transport3', last=230)
        MI = load(wb, 'Manual inputs', last=380)
    SRC_ISO = D[cell('D644')]
    assert re.fullmatch(r'[A-Z]{3}', SRC_ISO), SRC_ISO
    mv = lambda ref, o=0: M.get((cell(ref)[0] + o, cell(ref)[1]))
    dv = lambda ref: D.get(cell(ref))

    def label(r, text, col=3):
        got = str(M.get((r, col), '')).strip()
        assert got.startswith(text), (r, got, text)

    # ------------------------------------------------------------ Transport1 (all countries, 2022-2025)
    head = {c: v for (r, c), v in T1.items() if r == 1}
    rows1 = sorted({r for (r, c) in T1 if r > 1})
    names, data, srcs = {}, {}, {}
    for r in rows1:
        iso, yr = T1.get((r, 1)), T1.get((r, 2))
        if not iso or not num(yr):
            continue
        names[iso] = T1.get((r, 0))
        for c, var in head.items():
            if c < 3:
                continue
            v = T1.get((r, c))
            dest = srcs if 'source' in str(var) else data
            dest.setdefault((iso, var), {})[int(yr)] = v
    y1 = [2022, 2023, 2024, 2025]
    vars1 = [head[c] for c in sorted(head) if c >= 3]
    out = []
    for iso in sorted(names):
        for var in vars1:
            if 'source' in str(var):
                continue
            vals = data.get((iso, var), {})
            assert all(v is None or num(v) for v in vals.values()), (iso, var, vals)
            out.append([iso, names[iso], var] + ['' if vals.get(y) is None else vals[y] for y in y1])
    write('transport_data.csv', ['iso', 'country', 'variable'] + y1, out)
    out = []
    for iso in sorted(names):
        for var in vars1:
            if 'source' in str(var):
                vals = srcs.get((iso, var), {})
                out.append([iso, names[iso], var] + [vals.get(y, '') for y in y1])
    write('transport_data_sources.csv', ['iso', 'country', 'variable'] + y1, out)

    # ------------------------------------------------------------ Transport2 (vehicle prices, 2022-2040)
    head2 = {c: v for (r, c), v in T2.items() if r == 1}
    assert head2[1] == 'cpat_ccode3' and head2[2] == 'year', head2
    pr = {}
    for (r, c), v in T2.items():
        if r > 1 and c >= 3:
            iso, yr = T2.get((r, 1)), T2.get((r, 2))
            pr.setdefault((iso, head2[c]), {})[int(yr)] = v
    y2 = list(range(2022, 2041))
    out = [[iso, var] + [vals.get(y, '') for y in y2] for (iso, var), vals in sorted(pr.items())]
    write('vehicle_prices.csv', ['iso', 'variable'] + y2, out)

    # ------------------------------------------------------------ Transport3 (range anxiety per country)
    assert T3[(2, 7)] == 'Range anxiety' and T3[(2, 13)] == 'Range anxiety' and T3[(2, 19)] == 'Range anxiety'
    by_name = {n: i for i, n in names.items()}
    with open(os.path.join(DATA, 'countries.csv'), encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            by_name.setdefault(row['name'], row['code'])
    alias = {'Turkey': 'TUR', 'Turkiye': 'TUR', 'Czech Republic': 'CZE', 'Swaziland': 'SWZ', 'Cape Verde': 'CPV',
             'Macedonia': 'MKD', 'Kyrgyzstan': 'KGZ', 'Slovakia': 'SVK', 'Lao PDR': 'LAO', 'Russia': 'RUS'}
    out, miss = [], []
    for r in range(5, 227):
        name = T3.get((r, 0))
        if not name or not num(T3.get((r, 7))):
            continue
        iso = by_name.get(name) or alias.get(name)
        if not iso:
            miss.append(name)
            continue
        g = lambda c: T3.get((r, c), '')
        out.append([iso, name, g(7), g(13), g(19), g(2), g(3), g(8), g(9), g(14), g(15), f'Transport3 row {r}'])
    ra_cols = ['iso', 'country', 'passenger', 'freight', 'cycle', 'pass_actual', 'pass_calc', 'freight_actual',
               'freight_calc', 'cycle_actual', 'cycle_calc', 'source']
    write('range_anxiety.csv', ra_cols, out)
    if miss:
        print('  range_anxiety: no iso for', miss)
    avg = [sum(float(x[i]) for x in out) / len(out) for i in (2, 3, 4)]

    # ------------------------------------------------------------ parameters
    params = []
    for key, cells, unit, desc in SIDE:
        for c, ref in zip(CLS, cells):
            if ref is None:
                continue
            v = mv(ref)
            assert v == mv(ref, OFF), (ref, v, mv(ref, OFF))
            params.append([key.format(c=c), v, unit, desc.format(d=DCOL[c]), f'Mitigation {ref}', 'default'])
    for key, ref, unit, desc in SIDE_SINGLE:
        v = mv(ref)
        assert v == mv(ref, OFF), ref
        params.append([key, v, unit, desc, f'Mitigation {ref}', 'default'])
    assert abs(mv('T4329') - (-1.72 - 1.27 - 1.08 - 0.99) / 4) < 1e-15 and abs(mv('T4330') - 0.5725) < 1e-15
    for key, ref, unit, desc in DASH:
        params.append([key, dv(ref), unit, desc, f'Dashboard {ref}', 'default'])
    for key, val, unit, desc, cells in LITERALS:
        params.append([key, val, unit, desc, cells, 'default'])
    for c, v in zip(CLS, avg):
        params.append([f'ra_avg|{c}', v, 'USD/vehicle',
                       'range anxiety, average of Transport3 rows 5-226 (legacy fallback when a country has no value)',
                       'Transport3 H3/N3/T3 (IFERROR ... AVERAGE)', 'default'])
    for key, val, unit, desc in NOTE:
        params.append([key, val, unit, desc, 'Transportation_methodology.docx', 'note'])
    # checks of the side table against the Dashboard and of the policy-dependent cells
    for ref, dref in (('J4322', 'G542'), ('J4324', 'G543'), ('P4322', 'G551'), ('T4327', 'L554'), ('V4328', 'L556'),
                      ('P4317', 'G97'), ('P4318', 'G98'), ('Z4322', 'Q552'), ('J4332', 'L551')):
        assert mv(ref) == dv(dref), (ref, dref)
    write('transport_params.csv', ['key', 'value', 'unit', 'description', 'legacy_cell', 'use'], params)

    # ------------------------------------------------------------ global paths
    label(2051, 'BEV - light, fuel economy'); label(2095, 'BEV - freight, fuel economy')
    label(2122, 'BEV - 2-3 wheeler, new, fuel economy'); label(2170, 'Charging station costs')
    mi_col = {y: 9 + (y - 2022) for y in YEARS}      # Manual inputs J (2022) .. AC (2041)
    assert all(MI[(374, mi_col[y])] == y for y in YEARS)
    paths = []
    for key, r, desc in (('bev_fe_new|pass', 375, 'BEV fuel economy of new vehicles, passenger/light (km/kWh)'),
                         ('bev_fe_new|fre', 376, 'BEV fuel economy of new vehicles, freight (km/kWh)'),
                         ('bev_fe_new|cyc', 377, 'BEV fuel economy of new vehicles, 2-3 wheeler (km/kWh)')):
        assert str(MI[(r, 3)]).startswith('BEV'), MI[(r, 3)]
        paths.append([key, 'km/kWh', desc, f'Manual inputs row {r}'] + [MI[(r, mi_col[y])] for y in YEARS])
    for key, r, unit, desc in (('bev_fe|light', 2051, 'km/kWh', 'BEV fuel economy, light vehicles (data years used)'),
                               ('bev_fe|fre', 2095, 'km/kWh', 'BEV fuel economy, freight (data years used)'),
                               ('bev_fe|cyc', 2122, 'km/kWh', 'BEV fuel economy, 2-3 wheeler (data years used)'),
                               ('ch_cost_port', 2170, 'USD/port', 'charging-station cost per port')):
        paths.append([key, unit, desc, f'Mitigation row {r}'] + [M[(r, COL[y])] for y in YEARS])
    write('transport_paths.csv', ['key', 'unit', 'description', 'legacy_cell'] + YEARS, paths)

    # ------------------------------------------------------------ legacy reference (cached values, both runs)
    ref = []
    assert str(M[(2173, 1)]) == 'Baseline' and M[(2173, 2)] == 1, M.get((2173, 1))
    assert str(M[(2173 + OFF, 1)]) != 'Baseline' and M[(2173 + OFF, 2)] > 1, M.get((2173 + OFF, 1))
    assert str(M[(4302, 1)]).startswith('Transport sector') and str(M[(4302 + OFF, 1)]).startswith('Transport sector')
    for run, o in (('base', 0), ('pol', OFF)):
        for r in range(SEC[0], SEC[1] + 1):
            vals = [M.get((r + o, COL[y])) for y in YEARS]
            if any(num(v) for v in vals) and not (r in (4334, 4358, 4409, 4437, 4450, 4478, 4496, 4507, 4584,
                                                         4626, 4683, 4738, 4874, 4954, 5009, 5090, 5143, 5175,
                                                         5229, 5271, 5305, 5320, 5353, 5169, 5170, 5171, 5172,
                                                         5173)):     # 5169-5173: side table (scalars below)
                assert str(M.get((r + o, 3), '')) == str(M.get((r, 3), '')), r
                ref.append([f'r{r}', run, r + o, str(M.get((r, 3), ''))[:60]] +
                           ['' if not num(v) else v for v in vals])
        for c in SCALARS:
            rr, cc = cell(c)
            v = M.get((rr + o, cc))
            ref.append([f'c{c}', run, f'{re.sub(r"[0-9]", "", c)}{rr + o}', 'scalar'] +
                       [v if num(v) else ''] + [''] * (len(YEARS) - 1))
        for r in range(KEYB[0], KEYB[1] + 1):
            if 2017 <= r <= 2031:
                continue                                  # columns L/M/N are share/ktoe/bln liter: scalars below
            vals = [M.get((r, COL[y])) for y in YEARS]
            if any(num(v) for v in vals) and r not in (2033, 2091, 2120, 2139, 2149):
                ref.append([f'r{r}', run, r, str(M.get((r, 3), ''))[:60]] + ['' if not num(v) else v for v in vals])
        for c in SCALARS_KEYB:
            rr, cc = cell(c)
            v = M.get((rr, cc))
            ref.append([f'c{c}', run, c, 'scalar'] + [v if num(v) else ''] + [''] * (len(YEARS) - 1))
        # legacy inputs from the rest of Mitigation
        for key, r, lab in IN_RUN:
            if lab:
                label(r + o, lab)
            ref.append([f'in|{key}', run, r + o, str(M.get((r + o, 3), ''))[:60]] +
                       [M.get((r + o, COL[y]), 0.0) or 0.0 for y in YEARS])
            if key == 'gdp_growth':
                ref.append([f'in|{key}_2021', run, f'K{r + o}', 'scalar'] + [M.get((r + o, COL[2021]), 0.0) or 0.0]
                           + [''] * (len(YEARS) - 1))
        for key, r, lab in IN_SHARED:
            label(r, lab)
            ref.append([f'in|{key}', run, r, lab] + [M[(r, COL[y])] if num(M.get((r, COL[y]))) else '' for y in YEARS])
        ref.append(['in|scen', run, f'C{2173 + o}', 'scalar'] + [M[(2173 + o, 2)]] + [''] * (len(YEARS) - 1))
        ref.append(['in|c2227', run, f'C{2227 + o}', 'scalar (text in legacy: text > 1 is TRUE)'] +
                   [str(M[(2227 + o, 2)])] + [''] * (len(YEARS) - 1))
        waccs = [M[(r + o, 8)] for r in range(2988, 2997)]
        assert abs(sum(waccs) / 9 - mv('K4329', o)) < 1e-15
        ref.append(['in|wacc_avg', run, f'AVERAGE(I{2988 + o}:I{2996 + o})', 'scalar (freight discount rate K4329)'] +
                   [sum(waccs) / 9] + [''] * (len(YEARS) - 1))
        for key, c, lab, desc in IN_CELLS:
            rr, cc = cell(c)
            if lab:
                assert M[(rr, 6)] == lab, (c, M.get((rr, 6)))
            ref.append([f'in|{key}', run, c, desc] + [M[(rr, cc)]] + [''] * (len(YEARS) - 1))
        assert M[(581, 6)] == 'rod' and M[(583, 2)] == 'ele'
        ref.append(['in|ra|pass', run, 'N4354', 'range anxiety start (Transport3!H3)'] + [mv('N4354', o)] + [''] * 19)
        ref.append(['in|ra|fre', run, 'N4355', 'range anxiety start (Transport3!N3)'] + [mv('N4355', o)] + [''] * 19)
        ref.append(['in|ra|cyc', run, 'N4356', 'range anxiety start (Transport3!T3)'] + [mv('N4356', o)] + [''] * 19)
    write('legacy_transport_reference.csv', ['key', 'run', 'legacy_row', 'description'] + YEARS, ref)
    print(f'source {SRC}; legacy run country {SRC_ISO}')


if __name__ == '__main__':
    main()
