"""v2.8: data for the non-CO2 GHG and methane rows of CPAT-AI-Mitigation-Prototype (Methods, chapter Emissions).

Source: legacy CPAT `excel_ai/legacy/workbooks/CPAT 1.0pre_465_NoPropData.xlsb` (read-only; v8.5, LD41: was 456), values:
- `GHGs` rows 8-946: GHG inventory by country, year, UNFCCC category and gas (Mt CO2e; legacy key inputs 7 read
  columns H:AZ by position 1-43)                                                    -> data/ghg_inventory.csv
- `CH4Inputs`: methane abatement curves (avg_pow_a, avg_pow_b, per_flare) and the shares used to split
  inventory CH4 by source (per_upstream_og ... per_rice), by country and source       -> data/ch4_inputs.csv
- `EF_PM`: combustion emission factors of the country (kt per PJ, base value `FE in` and 2050 value `FE fin`), every
  pollutant; v8.5: the 465 file holds all countries (456: Egypt only): the rows of SRC_ISO are kept                             -> data/ef_nonco2.csv
- `UNPop` (rows below the header `CPAT code`): population by country and year (thousands; UN WPP)              -> data/population.csv
- `EF_GHG` (gwp100 rows): GWP100 of the local pollutants by GAINS region                -> data/gwp_pollutants.csv
- `Countries` column O: GAINS region of each country                                   -> data/gains_region.csv
- `Mitigation` rows 503-509 (energy balance of the base year, ktoe: imports, production, exports, ...) of the
  country of the legacy run (Egypt)                                                    -> data/energy_balance.csv

    python extract_ghg.py
"""
import csv
import os

from pyxlsb import open_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LEGACY = os.path.join(HERE, '..', 'legacy', 'workbooks', 'CPAT 1.0pre_465_NoPropData.xlsb')   # v8.5 (LD41): was 456
OUT = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts')
SRC_ISO = 'EGY'   # v3.3: country of the legacy run in the source file: the key (column country) of the rows written

CATS = ['enr', 'ipr', 'agr', 'lucf', 'wst', 'oth', 'tinc', 'texc']   # legacy order of the column groups
GASES = ['co2', 'ch4', 'n2o', 'fga', 'tot']
GHG_COLS = [f'{c}.{g}' for c in CATS for g in GASES] + ['fug.co2', 'fug.ch4', 'fug.n2o']   # positions 1-43


def rows(sheet):
    with open_workbook(LEGACY) as wb, wb.get_sheet(sheet) as sh:
        for row in sh.rows(sparse=True):
            if row:
                yield row[0].r + 1, {c.c: c.v for c in row if c.v is not None}


def write(name, header, data):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(data)
    print(f'wrote data/{name}: {len(data)} rows')


def num(v):
    return v if isinstance(v, (int, float)) else ''


def main():
    inv = []
    for r, v in rows('GHGs'):
        if 8 <= r <= 946 and isinstance(v.get(3), str) and isinstance(v.get(4), float):
            inv.append([v[3], int(v[4])] + [num(v.get(7 + k)) for k in range(len(GHG_COLS))])
    write('ghg_inventory.csv', ['iso', 'year'] + GHG_COLS, inv)

    ch4, head = [], None
    for r, v in rows('CH4Inputs'):
        if r == 1:
            head = [v.get(k) for k in range(12)]
        elif isinstance(v.get(1), str):
            ch4.append([v.get(1), v.get(2)] + [num(v.get(k)) for k in range(3, 12)])
    write('ch4_inputs.csv', ['iso', 'source'] + head[3:12], ch4)

    ef = [[v[1], v[2], v[3], v[4], num(v.get(5)), num(v.get(6))] for r, v in rows('EF_PM')
          if r >= 3 and isinstance(v.get(4), str) and isinstance(v.get(5), float) and v.get(1) == SRC_ISO.lower()]
    write('ef_nonco2.csv', ['country', 'subsector', 'fuel', 'pollutant', 'fe_in', 'fe_fin'], ef)

    pop, years = [], None
    for r, v in rows('UNPop'):
        if v.get(1) == 'CPAT code':                                 # header row: years from column E
            years = {k: int(x) for k, x in v.items() if isinstance(x, float) and k >= 4}
        elif years and isinstance(v.get(3), str) and len(v[3]) == 3:
            pop += [[v[3], y, v[k]] for k, y in years.items() if isinstance(v.get(k), float)]
    write('population.csv', ['iso', 'year', 'population_thousands'], pop)

    gwp = [[v[1], v[3], v[5]] for r, v in rows('EF_GHG')
           if isinstance(v.get(0), str) and '.gwp100.' in v[0] and isinstance(v.get(5), float)]
    write('gwp_pollutants.csv', ['region', 'pollutant', 'gwp100'], gwp)
    reg = [[v[3], v[14]] for r, v in rows('Countries')
           if isinstance(v.get(3), str) and len(v[3]) == 3 and isinstance(v.get(14), str) and v[3] != 'Code']
    write('gains_region.csv', ['iso', 'gains_region'], reg)

    bal = []
    for r, v in rows('Mitigation'):
        if r > 509:
            break
        if 503 <= r <= 509:
            bal.append([SRC_ISO, v.get(2)] + [num(v.get(k)) for k in (4, 5, 6, 7, 10, 13, 14, 15, 16)])
    write('energy_balance.csv', ['country', 'fuel', 'imports', 'production', 'exports', 'stock_change', 'tpes', 'stat_diff',
                                 'transfers', 'own_use', 'dist_loss'], bal)


if __name__ == '__main__':
    main()
