"""v0.3.1: data for the GDP effects of CPAT-AI-Mitigation-Prototype (section 16, Methods, chapter Macro and results).

Source: legacy CPAT `excel_ai/legacy/workbooks/CPAT 1.0pre_465_NoPropData.xlsb` (read-only), cached values. v0.8.5 (LD41):
moved from 456; Mitigation rows up to 5666 are the same in both files, the manual SCC path moved from row 17683
(456) to 17668 (465; row map legacy/bugfixes/data/rowmap_456_465.json).
- `Multipliers` rows 90-144 (median fiscal multipliers from MFMod by group: Global, HIC, UMIC, LMIC, LIC) and
  rows 149-203 (their standard deviations, the low/high adjustment), instruments EXC, PIT, CIT, VAT, CAPT, GNFS,
  TRNS, WAGE, lags 0-11 years; lags 12-19 hold the lag-11 value (legacy sheet rows 38-45 do the same)
                                                                                      -> data/multipliers.csv
- `Mitigation` rows 465 and 464 (baseline GDP, real, USD bn and LCU bn, IMF WEO; v0.3.13: 464) of the country of the legacy run (Egypt)
                                                                                      -> data/gdp_level.csv

    python extract_gdp.py
"""
import csv
import os

from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', 'legacy', 'workbooks', 'CPAT 1.0pre_465_NoPropData.xlsb')   # v0.8.5 (LD41): was 456
OUT = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
SRC_ISO = 'EGY'   # v0.3.3: country of the source files (legacy run, kernel): the key of the rows written
GROUPS = ['Global', 'HIC', 'UMIC', 'LMIC', 'LIC']
STATS = {'median': 90, 'sd': 149}          # first group header row of each table
NLAG, NDATA = 20, 12                       # lags written (0-19), lags in the legacy tables (0-11)
GDP_ROW, GDP_COL0, GDP_YEAR0 = 465, 9, 2020    # legacy Mitigation row 465: column J = 2020
SCC_ROW = 17668                                # v0.8.5: manual SCC path (456: row 17683)


def rows(sheet, last):
    with open_workbook(LEGACY) as wb, wb.get_sheet(sheet) as sh:
        for row in sh.rows(sparse=True):
            if row:
                r = row[0].r + 1
                if r > last:
                    break
                yield r, {c.c: c.v for c in row if c.v is not None}


def write(name, header, data):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(header)
        w.writerows(data)
    print(f'wrote data/{name}: {len(data)} rows')


def main():
    sheet = dict(rows('Multipliers', 205))
    out = []
    for stat, r0 in STATS.items():
        group = None
        for r in range(r0, r0 + 56):
            v = sheet.get(r, {})
            if v.get(1) in GROUPS and len(v) == 1:
                group = v[1]
            elif group and isinstance(v.get(1), str) and isinstance(v.get(3), float):
                vals = [float(v.get(3 + k, 0.0)) for k in range(NDATA)]
                vals += [vals[-1]] * (NLAG - NDATA)
                out.append([group.lower(), stat, v[1].lower()] + vals)
    assert len(out) == 2 * len(GROUPS) * 8, len(out)
    write('multipliers.csv', ['group', 'stat', 'instrument'] + [f'lag{k}' for k in range(NLAG)], out)
    mit = dict(rows('Mitigation', GDP_ROW))
    years = list(range(2021, 2042))
    out = []
    for row, code, key, lab, unit in ((GDP_ROW, 'gdpl.base.usd', 'gdp_usd', 'Baseline GDP, real', 'USD bn'),
                                      (GDP_ROW - 1, 'gdpl.base.lcu', 'gdp_lcu', 'Baseline GDP, real, local currency',
                                       'LCU bn')):     # v0.3.13: row 464 (header rows of Mitigation)
        v = mit[row]
        assert v.get(2) == code, v.get(2)
        out.append([f'{SRC_ISO}|{key}', SRC_ISO, lab, unit, f'legacy Mitigation row {row} (IMF WEO, cached values)']
                   + [v[GDP_COL0 + y - GDP_YEAR0] for y in years])
    tb = dict(rows('Mitigation', 743))              # v0.3.16: energy trade balance and share traded (rows 741-743)
    for row, code, lab in ((741, 'nga', 'Natural gas'), (742, 'oil', 'Oil products'), (743, 'coa', 'Coal')):
        v = tb[row]
        assert v.get(3) == lab, v.get(3)
        out.append([f'{SRC_ISO}|tb_{code}', SRC_ISO, f'Energy trade balance (exports - imports), {lab}', 'USD bn real',
                    f'legacy Mitigation row {row} (cached values)'] + [v[GDP_COL0 + y - GDP_YEAR0] for y in years])
        out.append([f'{SRC_ISO}|ts_{code}', SRC_ISO, f'Share traded (import share of a change in use), {lab}', 'share',
                    f'legacy Mitigation row {row}, column H'] + [v[7]] * len(years))
    man = dict(rows('Mitigation', SCC_ROW))[SCC_ROW]   # v0.3.17: manual SCC path (legacy row SCC_ROW, real USD per tCO2)
    assert man.get(3) == 'Manual', man.get(3)
    out.append([f'{SRC_ISO}|scc_manual', SRC_ISO, 'Social cost of carbon, manual path', 'USD per tCO2 real',
                f'legacy Mitigation row {SCC_ROW} (cached values)'] + [man.get(GDP_COL0 + y - GDP_YEAR0, '') for y in years])
    write('gdp_level.csv', ['key', 'country', 'variable', 'unit', 'source'] + years, out)
    scc = []                                       # v0.3.17: Ricke et al. (2018) country SCC, sheet SCC
    for r, v in rows('SCC', 1000):
        if r >= 8 and isinstance(v.get(1), str) and '.' in v.get(1, ''):
            scc.append([v[1], v[2], v[3], v[4], v[5]])
    write('scc.csv', ['code', 'iso3', 'prtp', 'eta', 'central_usd_per_tco2'], scc)


if __name__ == '__main__':
    main()
