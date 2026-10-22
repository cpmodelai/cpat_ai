"""v3.3: ETS semi-elasticities of emissions to the carbon price, by country and ETS sector group.

Source: legacy CPAT `excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb` (read-only), sheet `ETS+LTS`
rows 82-256 (one row per country: country code in column C, lower case; semi-elasticities of Power, Transport,
Residential and Industry in columns D-G; header codes pow, tra, res, ind in row 81). Legacy Mitigation rows 1815-1831
look the table up by country and sector group (food and services use Industry).        -> data/ets_semi.csv

    python extract_ets.py
"""
import csv
import os

from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', 'legacy', 'workbooks', 'CPAT 1.0pre_456_NoPropData.xlsb')
OUT = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts', 'ets_semi.csv')
HDR, R0, R1 = 81, 82, 256             # header row (codes), first and last country row
GROUPS = ['pow', 'tra', 'res', 'ind']  # columns D-G


def main():
    rows = {}
    with open_workbook(LEGACY) as wb, wb.get_sheet('ETS+LTS') as sh:
        for row in sh.rows(sparse=True):
            if not row:
                continue
            r = row[0].r + 1
            if r > R1:
                break
            if r == HDR or r >= R0:
                rows[r] = {c.c: c.v for c in row if c.v is not None}
    assert [rows[HDR].get(3 + j) for j in range(4)] == GROUPS, rows[HDR]
    out = []
    for r in range(R0, R1 + 1):
        v = rows.get(r, {})
        if not v.get(2):
            continue
        out.append([str(v[2]).upper(), v.get(1, '')] + [v.get(3 + j, '') for j in range(4)]
                   + [f'ETS+LTS row {r}'])
    with open(OUT, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['iso', 'country'] + GROUPS + ['source'])
        w.writerows(out)
    print(f'wrote {OUT}: {len(out)} countries')


if __name__ == '__main__':
    main()
