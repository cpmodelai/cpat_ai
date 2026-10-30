"""v0.4.5: data tables copied unchanged from legacy CPAT (CPAT 1.0pre_465_NoPropData.xlsb; 456 until v0.8.4), so that the full
(proprietary, all-country) legacy tables can be pasted over them: the workbook keeps each legacy table's columns and
order from column A (same column letters as legacy; leading empty legacy columns stay empty), header in row 3, data
from row 4; where legacy has no unique key, the workbook adds a key formula column right of the table.
Writes data/legacy_<Tab>.csv (header + data rows):
  Balances     legacy Balances rows 13+ (energy balance by flow and fuel; NoPropData: Egypt)
  EF_PM        legacy EF_PM rows 2+ (combustion emission factors of non-CO2 gases and local pollutants; v0.9.0: all
               countries and regions, as the prototype looks up country, else region, else world like legacy)
  EnergyCons   legacy EnergyCons layout (empty in NoPropData): filled from Balances with legacy's mapping
               (Mitigation rows 529-601: subsector = Balances flow; pow = -power; ftr = -(ownuse + heat))
  IO_GTAP, HHSurvey, ASPIRE, WHOCooking   legacy tabs (Egypt in NoPropData)
  HH_Elast, GDPRatios                     legacy tabs (all countries)
  SCC, UNPop, CH4Inputs, GHGs (rows 8-947), Transport1, Transport2, EF_GHG   legacy tabs (all countries)
  OilProductShares   (v0.4.12) household share of each oil product by country (all countries; legacy Mitigation rows
               801-816: VAT applies to this share)
  WEO_NGDP_D   the GDP deflator rows (NGDP_D.A) of legacy WEO, all countries, legacy WEO columns
  WEO          (v0.4.6) the whole legacy WEO table (header row 9; all countries and series)
v0.4.6: tabs with several legacy tables are kept at their legacy cell addresses from row 3 (rows 1-2 are the workbook's
title rows): data/legacy_<Tab>_cells.csv (row, column, value) for Countries, Elasticities, ETS+LTS, Multipliers,
Prices_int, ECP (from row 3) and Transport3 (stored results, rows 5+).
v0.5.2: the legacy tab 'Manual inputs' rows 3-378 at its legacy addresses: data/legacy_ManualInputs_cells.csv (row, column,
value, formula: 1 where the legacy cell is a formula, its cached value given). Only this part:
    python3 extract_legacy_tables.py manual
v0.5.7 (NDC comparison, item 8B): the three NDC submission tables of legacy tab NDCs (rows 48-242 latest, 250-444 second,
451-644 first round; columns C-P) stacked with a round column: data/legacy_NDCs.csv; the historical GHG table of legacy
tab GHGs (rows 954-1189: GHGs excl./incl. LULUCF, CO2 excl. LULUCF, energy CO2 by year): data/legacy_GHGHist.csv.
Only this part:
    python3 extract_legacy_tables.py ndc
v0.8.5 (LD41, 2026-10-29): source moved from CPAT 1.0pre_456 to CPAT 1.0pre_465 (sheet layouts of every tab read here are
the same in both files). Two exceptions:
  - HHSurvey and HH_Elast are still read from 456: the 465 NoPropData file holds only their header rows.
  - EF_PM, IO_GTAP, ASPIRE and WHOCooking hold all countries in 465 (Egypt only in 456): the rows of the country of
    the legacy run (Egypt) are kept (EGYPT_ONLY), so the prototype tables keep their size; the Egypt rows are the same
    as in 456. Set EGYPT_ONLY = {} to write the all-country tables.
  - v0.9.0 (EF465): EF_PM is written whole (all countries and World Bank regions, legacy order; the 465 lookup range
    ends at row 39323, past the last data row): legacy Mitigation rows 1052-1663 take the factor of the country,
    else of its region, else of the world. Only this table:
    python3 extract_legacy_tables.py efpm"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'data', 'scripts'))
from legacy_csv import legacy_dir, save_to_tidy  # noqa: E402,F401  (the data edition's tidy/ in the legacy CSV form)
import csv, os
from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', '..', 'data', 'Public01', 'legacy', 'CPAT 1.0pre_465_Public01.xlsb')   # v0.8.5 (LD41): was 456
LEGACY_456 = os.path.join(HERE, '..', 'legacy', 'workbooks', 'CPAT 1.0pre_456_NoPropData.xlsb')
FROM_456 = ('HHSurvey', 'HH_Elast')    # v0.8.5: empty (header only) in the 465 NoPropData file: still read from 456
EGYPT_ONLY = {'IO_GTAP': (1, 'egy'), 'ASPIRE': (2, 'EGY'), 'WHOCooking': (1, 'EGY')}   # v0.8.5 (v0.9.0: EF_PM whole):
# all countries in 465: keep the rows whose column (0-based) holds the code of the legacy run's country
DATA = legacy_dir()
HEADER_ROW = {'Balances': 13, 'EF_PM': 2, 'IO_GTAP': 1, 'HHSurvey': 1, 'HH_Elast': 1, 'ASPIRE': 1,
              'WHOCooking': 1, 'GDPRatios': 1, 'WEO': 9, 'SCC': 7, 'UNPop': 6, 'CH4Inputs': 1, 'GHGs': 7,
              'Transport1': 1, 'Transport2': 1, 'EF_GHG': 3, 'OilProductShares': 1}   # 1-based row of each legacy table's header
AT_ADDRESS = {'Countries': 3, 'Elasticities': 3, 'ETS+LTS': 3, 'Multipliers': 3, 'Prices_int': 3, 'ECP': 3,
              'Transport3': 5, 'Power': 3, 'CoC': 3, 'GHGs': 3}   # v0.4.7 (v0.4.7: Power, CoC, GHGs): first legacy row kept
CONTIGUOUS = {'GHGs'}            # the table ends at its first empty row (other tables follow below it in legacy)
SUB_FLOWS = {'rod': ['road'], 'ral': ['rail'], 'avi': ['domesair'], 'nav': ['domesnav'], 'res': ['resident'],
             'foo': ['food_forest'], 'srv': ['services'], 'mch': ['mining_chemicals'], 'irn': ['ironstl'],
             'nfm': ['nonferrmet'], 'mac': ['machinery'], 'cem': ['cement'], 'omn': ['other_manufact'],
             'cst': ['construc'], 'oen': ['ononspec'], 'ftr': ['-ownuse', '-heat'], 'pow': ['-power'],
             'elec': ['eloutput'], 'wav': ['worldav'], 'neu': ['nonenuse']}   # legacy Mitigation rows 529-601
ENC_FUELS = [('ele', 'ecy', 'Electricity'), ('coa', 'coa', 'Coal'), ('nga', 'nga', 'Natural gas'),
             ('oop', 'oop', 'Other oil products'), ('gso', 'gso', 'Gasoline'), ('die', 'die', 'Diesel'),
             ('ker', 'ker', 'Kerosene'), ('lpg', 'lpg', 'LPG'), ('jfu', 'jfu', 'Jet fuel'), ('wnd', 'wnd', 'Wind'),
             ('sol', 'sol', 'Solar'), ('hyd', 'hyd', 'Hydro'), ('ore', 'ore', 'Other renewables'),
             ('nuc', 'nuc', 'Nuclear'), ('bio', 'bio', 'Biomass'), ('bgs', 'bgs', '- in which: biogasoline'),
             ('bdi', 'bdi', '- in which: biodiesel'), ('obf', 'obf', '- in which: other liquid biofuels'),
             ('heat', 'hea', 'Heat')]                          # legacy Mitigation rows 583-601 (code, Balances col)
ENC_HEADER = ['CPAT Code', 'Year', 'CountryName', 'FuelType', 'elec', 'pow', 'rod', 'ral', 'avi', 'nav', 'res',
              'foo', 'srv', 'mch', 'irn', 'nfm', 'mac', 'cem', 'omn', 'cst', 'ftr', 'oen', 'wav', 'neu']


def table(wb, name):
    """Header and data rows of a legacy table (trailing empty columns dropped; empty rows skipped)."""
    with wb.get_sheet(name) as sh:
        rows = [[c.v for c in r] for r in sh.rows()]
    h = HEADER_ROW[name] - 1
    head = rows[h]
    n = max(j for j, v in enumerate(head) if v not in (None, '')) + 1
    body = [r[:n] + [None] * (n - len(r[:n])) for r in rows[h + 1:]]
    if name in CONTIGUOUS:
        body = body[:next((i for i, r in enumerate(body) if all(v in (None, '') for v in r)), len(body))]
    if name in EGYPT_ONLY:                                           # v0.8.5
        j, code = EGYPT_ONLY[name]
        body = [r for r in body if r[j] == code]
    return head[:n], [r for r in body if any(v not in (None, '') for v in r)]


def clean(v):
    if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
        return int(v)
    return '' if v is None else v


def write(name, head, body):
    with open(os.path.join(DATA, f'legacy_{name}.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow([clean(v) for v in head])
        w.writerows([[clean(v) for v in r] for r in body])
    print(f'legacy_{name}.csv: {len(body)} rows, {len(head)} columns')


MANUAL_ROWS = (3, 378)          # v0.5.2: legacy Manual inputs, rows kept (the sheet ends at row 378)


def manual_inputs(wb):
    """v0.5.2: every cell of the legacy Manual inputs tab, rows 3-378, with a flag for formula cells (cached value)."""
    from pyxlsb import biff12
    from pyxlsb.worksheet import Cell
    cells = []
    with wb.get_sheet('Manual inputs') as sh:
        sh._reader.seek(sh._data_offset, os.SEEK_SET)
        r = -1
        for item in sh._reader:
            if item[0] == biff12.ROW:
                r = item[1].r
            elif biff12.BLANK <= item[0] <= biff12.FORMULA_BOOLERR:
                v = sh._stringtable[item[1].v] if item[0] == biff12.STRING and sh._stringtable else item[1].v
                if item[0] in (biff12.BOOLERR, biff12.FORMULA_BOOLERR) and not isinstance(v, str):
                    v = hex(v)
                if v not in (None, '') and MANUAL_ROWS[0] <= r + 1 <= MANUAL_ROWS[1]:
                    cells.append((r + 1, item[1].c + 1, clean(v), int(item[0] >= biff12.FORMULA_STRING)))
            elif item[0] == biff12.SHEETDATA_END:
                break
    with open(os.path.join(DATA, 'legacy_ManualInputs_cells.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['row', 'col', 'value', 'formula'])
        w.writerows(sorted(cells))
    print(f'legacy_ManualInputs_cells.csv: {len(cells)} cells, rows {MANUAL_ROWS[0]}-{MANUAL_ROWS[1]}')


NDC_ROUNDS = [('Latest*', 48, 242), ('Second round', 250, 444), ('First round', 451, 644)]
NDC_HEAD = ['round', 'country', 'code', 'type', 'ty1', 'ty2', 'ref', 'cond', 'u1', 'c1', 'u2', 'c2', 'lulucf', 'gases',
            'submission']                     # legacy NDCs columns C-P (short names, looked up by name)
HIST_GROUPS = [('exc', 7, 15), ('inc', 15, 23), ('co2', 23, 36), ('eco2', 36, 47)]   # legacy GHGs columns H-AU (0-based)


def ndc_tables(wb):
    """v0.5.7: legacy NDC submissions (three rounds stacked) and historical GHGs (legacy GHGs rows 954-1189)."""
    with wb.get_sheet('NDCs') as sh:
        rows = [[c.v for c in r] for r in sh.rows()]
    body = []
    for lab, a, b in NDC_ROUNDS:
        for r in rows[a - 1:b]:
            r = (r + [None] * 16)[2:16]
            if r[1] not in (None, ''):
                body.append([lab] + r)
    write('NDCs', NDC_HEAD, body)
    with wb.get_sheet('GHGs') as sh:
        rows = [[c.v for c in r] for r in sh.rows()]
    yrs = (rows[953] + [None] * 50)[:50]
    head = ['country', 'iso'] + [f'{g}|{int(yrs[j])}' for g, a, b in HIST_GROUPS for j in range(a, b)]
    body = []
    for r in rows[954:1189]:
        r = (r + [None] * 50)[:50]
        if r[3] not in (None, ''):
            body.append([r[2], r[3]] + [r[j] for _g, a, b in HIST_GROUPS for j in range(a, b)])
    write('GHGHist', head, body)


def main():
    import sys
    if sys.argv[1:] == ['ndc']:
        with open_workbook(LEGACY) as wb:
            ndc_tables(wb)
        return
    if sys.argv[1:] == ['efpm']:                                   # v0.9.0 (EF465): EF_PM only
        with open_workbook(LEGACY) as wb:
            write('EF_PM', *table(wb, 'EF_PM'))
        return
    if sys.argv[1:] == ['manual']:
        with open_workbook(LEGACY) as wb:
            manual_inputs(wb)
        return
    with open_workbook(LEGACY_456) as wb456:                        # v0.8.5: tables the 465 NoPropData file lacks
        old = {name: table(wb456, name) for name in FROM_456}
    with open_workbook(LEGACY) as wb:
        manual_inputs(wb)
        for name in ('Balances', 'EF_PM', 'IO_GTAP', 'HHSurvey', 'HH_Elast', 'ASPIRE', 'WHOCooking', 'GDPRatios',
                     'SCC', 'UNPop', 'CH4Inputs', 'GHGs', 'Transport1', 'Transport2', 'EF_GHG', 'OilProductShares'):
            head, body = old[name] if name in FROM_456 else table(wb, name)
            if name == 'Balances':
                bal_head, bal = head, body
            write(name, head, body)
        head, body = table(wb, 'WEO')
        write('WEO_NGDP_D', head, [r for r in body if isinstance(r[3], str) and r[3].endswith('.NGDP_D.A')])
        write('WEO', head, body)                                        # v0.4.7: the whole table
        for name, r0 in AT_ADDRESS.items():                             # v0.4.7: tabs kept at legacy addresses
            with wb.get_sheet(name) as sh:
                cells = [(c.r + 1, c.c + 1, clean(c.v)) for row in sh.rows() for c in row
                         if c.v not in (None, '') and c.r + 1 >= r0]
            with open(os.path.join(DATA, f'legacy_{name}_cells.csv'), 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['row', 'col', 'value'])
                w.writerows(cells)
            print(f'legacy_{name}_cells.csv: {len(cells)} cells from row {r0}')
    col = {h: j for j, h in enumerate(bal_head)}
    rows = []
    by = {}
    for r in bal:
        by.setdefault((r[col['country_code']], r[col['year']], r[col['country']]), {})[r[col['flow_code']]] = r
    for (iso, year, cname), flows in sorted(by.items()):
        for code, bcol, label in ENC_FUELS:
            vals = []
            for sec in ENC_HEADER[4:]:
                v = 0.0
                for fl in SUB_FLOWS[sec]:
                    sign = -1 if fl.startswith('-') else 1
                    x = flows.get(fl.lstrip('-'), [None] * len(bal_head))[col[bcol]] if bcol in col else None
                    v += sign * (x or 0.0)
                vals.append(v)
            rows.append([f'{iso.lower()}.mit.enc.{code}', year, cname, label] + vals)
    write('EnergyCons', ENC_HEADER, rows)


if __name__ == '__main__':
    main()
