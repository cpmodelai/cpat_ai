"""
Export the four proprietary input tables of Coded CPAT into the layout of the
legacy CPAT workbook (`excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb`),
so they can be copy-pasted into the legacy data sheets.

    Coded CPAT CSV (DATA_PATH)    ->  legacy sheet   layout
    energy_consumption.csv        ->  EnergyCons     row 1 header, data from row 2; fuel rows x sector columns
    prices_dom.csv                ->  Prices_dom     rows 1-8 header, data from row 9; one row per country-year
    distn_hh_survey.csv (long)    ->  HHSurvey       row 1 header, data from row 2; wide (one column per variable)
    distn_io_gtap.csv (long)      ->  IO_GTAP        row 1 header, data from row 2; wide (one column per GTAP sector)

Every output sheet has the same name, header rows and cell positions as the
legacy sheet, so a whole sheet (or its data block) pastes onto the legacy
sheet at the same address. A ReadMe sheet lists the paste ranges and what was
left blank. Header layouts come from `legacy_layouts.json` (rebuilt from the
legacy workbook with --rebuild-layouts, which needs pyxlsb).

Run from data/:
    python scripts/export_to_legacy.py [--data DIR] [--out FILE] [--countries EGY KEN ...]
                                             [--energy-year 2022]
--data defaults to config.DATA_PATH (.env: dummy or REAL_DATA_PATH).
"""
import argparse
import csv
import datetime
import json
import os
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUTS_FILE = os.path.join(HERE, 'legacy_layouts.json')
LEGACY_XLSB = os.path.join(HERE, '..', '..', 'excel_ai', 'legacy', 'workbooks', 'CPAT 1.0pre_456_NoPropData.xlsb')

# coded fuel code -> legacy EnergyCons fuel code (legacy Mitigation C583:C601; heat is 'heat' there)
ENERGY_FUEL_TO_LEGACY = {'hea': 'heat'}
# columns of energy_consumption.csv that legacy computes itself (Mitigation row 602 'ren', column X 'Total
# energy-use territorial consumption'), so they are not exported
ENERGY_DERIVED_FUELS = ['ren']
ENERGY_DERIVED_SECTORS = ['total_energy_use']
PRICES_END_MARKER = '***'


# ---------------------------------------------------------------- layouts
def rebuild_layouts():
    """Read the header rows of the legacy data sheets (and the fuel labels of Mitigation rows 583-601) into
    legacy_layouts.json."""
    from pyxlsb import open_workbook

    def rows_of(wb, sheet, n_rows):
        out = []
        with wb.get_sheet(sheet) as sh:
            for i, row in enumerate(sh.rows()):
                if i >= n_rows:
                    break
                out.append([c.v for c in row])
        return [_trim(r) for r in out]

    def _trim(r):
        r = list(r)
        while r and r[-1] is None:
            r.pop()
        return r

    with open_workbook(LEGACY_XLSB) as wb:
        mit = rows_of(wb, 'Mitigation', 601)
        layouts = {
            '_comment': 'Header layouts of the legacy CPAT data sheets, read from '
                        'excel_ai/legacy/workbooks/CPAT 1.0pre_456_NoPropData.xlsb by '
                        'export_to_legacy.py --rebuild-layouts. Do not edit by hand.',
            'EnergyCons': {'header_rows': rows_of(wb, 'EnergyCons', 1), 'first_data_row': 2,
                           # (fuel code, label) in legacy Mitigation C583:D601 order
                           'fuels': [[mit[r][2], mit[r][3]] for r in range(582, 601)]},
            'Prices_dom': {'header_rows': rows_of(wb, 'Prices_dom', 8), 'first_data_row': 9},
            'HHSurvey': {'header_rows': rows_of(wb, 'HHSurvey', 1), 'first_data_row': 2},
            'IO_GTAP': {'header_rows': rows_of(wb, 'IO_GTAP', 1), 'first_data_row': 2},
        }
    with open(LAYOUTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(layouts, f, indent=1, ensure_ascii=False)
    print(f'wrote {LAYOUTS_FILE}')


def load_layouts():
    with open(LAYOUTS_FILE, encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- tables
def _read_csv(path, **kw):
    """pandas' default float parser can be a few ulps off; round_trip keeps every value equal to the CSV text."""
    return pd.read_csv(path, float_precision='round_trip', **kw)


def _country_names(data_dir):
    """CountryCode -> country name, from prices_dom.csv (the one proprietary table that carries names)."""
    p = _read_csv(os.path.join(data_dir, 'prices_dom.csv'), usecols=['CountryCode', 'countryname'])
    return dict(p.drop_duplicates('CountryCode').itertuples(index=False))


def _filter(df, col, countries, lower=False):
    if not countries:
        return df
    wanted = {c.lower() for c in countries} if lower else {c.upper() for c in countries}
    return df[df[col].isin(wanted)]


def energy_cons_rows(data_dir, layout, countries, year):
    """energy_consumption.csv (rows country x sector, columns fuels) -> EnergyCons (rows country x fuel,
    columns sectors). Key 'egy.mit.enc.ele' as legacy Mitigation B583 (LOWER(country)&".mit.enc."&fuel)."""
    header = layout['header_rows'][0]                       # CPAT Code, Year, CountryName, FuelType, elec ... neu
    sectors = header[4:]
    ec = _filter(_read_csv(os.path.join(data_dir, 'energy_consumption.csv')), 'CountryCode', countries)
    names = _country_names(data_dir)
    notes = []
    missing_sectors = [s for s in sectors if s not in set(ec['SectorCode'])]
    if missing_sectors:
        notes.append(f'EnergyCons: sector columns {", ".join(missing_sectors)} are not in energy_consumption.csv; '
                     'left blank (legacy Mitigation does not read them in Consumption mode).')
    extra = sorted(set(ec['SectorCode']) - set(sectors) - set(ENERGY_DERIVED_SECTORS))
    if extra:
        notes.append(f'EnergyCons: sectors {", ".join(extra)} have no legacy column; not exported.')
    fuel_cols = [c for c in ec.columns if c not in ('CountryCode', 'SectorCode')]
    legacy_fuels = [f for f, _ in layout['fuels']]
    labels = dict(layout['fuels'])
    coded_for_legacy = {ENERGY_FUEL_TO_LEGACY.get(f, f): f for f in fuel_cols if f not in ENERGY_DERIVED_FUELS}
    extra_f = sorted(set(coded_for_legacy) - set(legacy_fuels))
    if extra_f:
        notes.append(f'EnergyCons: fuels {", ".join(extra_f)} have no legacy row; not exported.')
    rows = []
    for country, g in ec.groupby('CountryCode', sort=False):
        g = g.set_index('SectorCode')
        for fuel in legacy_fuels:
            coded = coded_for_legacy.get(fuel)
            vals = [(_num(g.at[s, coded]) if coded is not None and s in g.index else None) for s in sectors]
            rows.append([f'{country.lower()}.mit.enc.{fuel}', year, names.get(country, country), labels[fuel]] + vals)
    return rows, notes


def prices_dom_rows(data_dir, layout, countries):
    """prices_dom.csv -> Prices_dom: the legacy columns in legacy order; columns not in the CSV left blank."""
    header = layout['header_rows'][-1]                     # codes row (row 8)
    p = _filter(_read_csv(os.path.join(data_dir, 'prices_dom.csv')), 'CountryCode', countries)
    keys = {'country_year', 'countrycode_weo', 'countrycode', 'countryname', 'year', PRICES_END_MARKER}
    blank = [h for h in header if h not in keys and h not in p.columns]
    extra = [c for c in p.columns if c not in header and c != 'CountryCode']
    notes = []
    if blank:
        notes.append(f'Prices_dom: {len(blank)} legacy columns are not in prices_dom.csv and are left blank: '
                     + ', '.join(blank) + '.')
    if extra:
        notes.append(f'Prices_dom: columns {", ".join(extra)} have no legacy column; not exported.')
    rows = []
    for rec in p.to_dict('records'):
        code, year = rec['CountryCode'], int(rec['year'])
        fixed = {'country_year': f'{code}{year}', 'countrycode_weo': code, 'countrycode': code,
                 'countryname': rec['countryname'], 'year': year, PRICES_END_MARKER: PRICES_END_MARKER}
        rows.append([fixed[h] if h in fixed else _num(rec.get(h)) for h in header])
    return rows, notes


def _wide(df, key_cols, var_col, val_col, legacy_cols):
    """Long -> wide in the order rows first appear, columns in legacy order (extra variables appended)."""
    code = key_cols[0]                                      # the row code is unique per legacy row
    keys = df.drop_duplicates(code)[key_cols]
    vals = df.pivot_table(index=code, columns=var_col, values=val_col, aggfunc='first', sort=False)
    w = keys.merge(vals, left_on=code, right_index=True, how='left')
    vars_present = list(dict.fromkeys(df[var_col]))
    cols = [c for c in legacy_cols if c in vars_present] + [c for c in vars_present if c not in legacy_cols]
    missing = [c for c in legacy_cols if c not in vars_present]
    return w, cols, missing


def hh_survey_rows(data_dir, layout, countries):
    header = layout['header_rows'][0]
    keys = header[:7]                                       # code, iso3, year, sample, type, stat_type, quant_cons
    hh = _filter(_read_csv(os.path.join(data_dir, 'distn_hh_survey.csv')), 'iso3', countries)
    w, cols, missing = _wide(hh, keys, 'variable', 'value', header[7:])
    return _rows_from_wide(w, keys, header[7:], cols, missing, 'HHSurvey', 'distn_hh_survey.csv')


def io_gtap_rows(data_dir, layout, countries):
    header = layout['header_rows'][0]
    keys = header[:4]                                       # dis, iso3, year, sector
    io = _filter(_read_csv(os.path.join(data_dir, 'distn_io_gtap.csv')), 'iso3', countries, lower=True)
    w, cols, missing = _wide(io, keys, 'gtap_sector', 'value', header[4:])
    return _rows_from_wide(w, keys, header[4:], cols, missing, 'IO_GTAP', 'distn_io_gtap.csv')


def _rows_from_wide(w, keys, legacy_cols, cols, missing, sheet, csv):
    notes = []
    if missing:
        notes.append(f'{sheet}: columns {", ".join(missing)} are not in {csv}; left blank.')
    extra = [c for c in cols if c not in legacy_cols]
    if extra:
        notes.append(f'{sheet}: variables {", ".join(extra)} have no legacy column; not exported.')
    rows = []
    for rec in w.to_dict('records'):
        rows.append([_num(rec[k]) for k in keys] + [_num(rec.get(c)) if c in cols else None for c in legacy_cols])
    return rows, notes


def _num(v):
    """Python scalar for openpyxl: NaN -> blank, whole-number floats in key columns stay floats (as legacy)."""
    if v is None:
        return None
    if isinstance(v, (float, np.floating)):
        return None if np.isnan(v) else float(v)
    if isinstance(v, np.integer):
        return int(v)
    return v


# ---------------------------------------------------------------- workbook
def _grid(layout, rows):
    """The sheet as a list of rows from row 1: header rows, blank rows up to the data, data rows."""
    grid = [list(h) for h in layout['header_rows']]
    grid += [[] for _ in range(layout['first_data_row'] - 1 - len(grid))]
    return grid + rows


def write_workbook(out_path, sheets):
    """One tab per legacy sheet, nothing else, so the file has exactly the legacy tabs."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, (layout, rows) in sheets.items():
        ws = wb.create_sheet(name)
        for r, row in enumerate(_grid(layout, rows), start=1):
            for c, v in enumerate(row, start=1):
                if v is not None:
                    ws.cell(r, c, v)
        ws.freeze_panes = ws.cell(layout['first_data_row'], 1)
    wb.save(out_path)
    sys.path.insert(0, os.path.join(HERE, '..', '..', 'excel_ai', 'shared'))
    import excel_lint
    excel_lint.check(out_path)                   # NORMS 3g


def write_csvs(csv_dir, sheets):
    """One CSV per legacy sheet (<sheet>.csv), cell for cell as the tab: header rows included."""
    os.makedirs(csv_dir, exist_ok=True)
    for name, (layout, rows) in sheets.items():
        with open(os.path.join(csv_dir, f'{name}.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            for row in _grid(layout, rows):
                w.writerow(['' if v is None else repr(v) if isinstance(v, float) else v for v in row])


def write_readme(path, sheets, notes, data_dir, countries, energy_year):
    lines = [
        ('CPAT legacy data export', True),
        (f'Created {datetime.date.today().isoformat()} by data/scripts/export_to_legacy.py', None),
        (f'Source folder: {data_dir}', None),
        (f'Countries: {", ".join(countries) if countries else "all in the source files"}', None),
        (f'EnergyCons year column: {energy_year} (energy_consumption.csv has no year)', None),
        ('', None),
        ('How to paste into legacy CPAT (CPAT 1.0pre_456 .xlsb)', True),
        ('Each sheet here has the same name, header rows and cell positions as the legacy data sheet. Copy the '
         'data block below and Paste Special > Values onto the legacy sheet at the same top-left cell. Clear the '
         'old data rows first if the new block is shorter.', None),
    ]
    for name, (layout, rows) in sheets.items():
        r0 = layout['first_data_row']
        ncol = max(len(h) for h in layout['header_rows'])
        last = openpyxl.utils.get_column_letter(ncol)
        rng = f'A{r0}:{last}{r0 + len(rows) - 1}' if rows else '(no rows)'
        hdr = 'header row 1' if r0 == 2 else f'header rows 1-{r0 - 1}'
        lines.append((f'  {name}: data {rng} ({len(rows)} rows); {hdr} as in legacy', None))
    lines += [
        ('', None),
        ('Legacy settings and checks', True),
        ('EnergyCons is read by legacy Mitigation rows 583-601 only when the Dashboard switch '
         'BalancesOrConsumption is not "Balances" (Mitigation C578). The IEA flow-level Balances sheet cannot be '
         'built from energy_consumption.csv (already aggregated to CPAT sectors).', None),
        ('In the NoPropData workbook some lookups into the stripped sheets were shrunk to row 1 (e.g. Mitigation '
         'AA583 =MATCH(B583,EnergyCons!$A$1:$A$1,0)). Pasting into that file needs those ranges widened to the data '
         'rows; the full (proprietary) workbook has them.', None),
        ('EnergyCons keys are LOWER(country)&".mit.enc."&fuel (Mitigation B583); heat uses "heat". Prices_dom '
         'countrycode_weo is set to the ISO code; check it for countries whose WEO code differs.', None),
        ('', None),
        ('Gaps in the source files', True),
    ]
    lines += [(n, None) for n in notes] or [('None', None)]
    with open(path, 'w', encoding='utf-8') as f:
        for text, heading in lines:
            f.write(f'\n## {text}\n\n' if heading and text != 'CPAT legacy data export' else
                    f'# {text}\n\n' if heading else f'{text}\n')


def export(data_dir, out_path, countries=None, energy_year=2022, csv_dir=None):
    """Write the four legacy tabs to out_path (and, with csv_dir, as four CSVs there), plus
    <out_path stem>_ReadMe.md with the paste ranges and the gaps."""
    layouts = load_layouts()
    sheets, notes = {}, []
    for name, build in (
            ('EnergyCons', lambda l: energy_cons_rows(data_dir, l, countries, energy_year)),
            ('Prices_dom', lambda l: prices_dom_rows(data_dir, l, countries)),
            ('HHSurvey', lambda l: hh_survey_rows(data_dir, l, countries)),
            ('IO_GTAP', lambda l: io_gtap_rows(data_dir, l, countries))):
        rows, n = build(layouts[name])
        sheets[name] = (layouts[name], rows)
        notes += n
        if not rows:
            notes.append(f'{name}: no rows for the selected countries.')
    write_workbook(out_path, sheets)
    if csv_dir:
        write_csvs(csv_dir, sheets)
    write_readme(os.path.splitext(out_path)[0] + '_ReadMe.md', sheets, notes, data_dir, countries, energy_year)
    return sheets, notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--data', help='folder with the Coded CPAT CSVs (default: config.DATA_PATH)')
    ap.add_argument('--out', default='CPAT_LegacyData.xlsx', help='output workbook (default: %(default)s)')
    ap.add_argument('--csv-dir', help='also write the four tabs as CSVs (<sheet>.csv) to this folder')
    ap.add_argument('--countries', nargs='*', help='ISO3 codes (default: all)')
    ap.add_argument('--energy-year', type=int, default=2022,
                    help='value of the EnergyCons Year column (default: %(default)s, the legacy base year)')
    ap.add_argument('--rebuild-layouts', action='store_true',
                    help='re-read legacy_layouts.json from the legacy workbook (needs pyxlsb) and exit')
    a = ap.parse_args(argv)
    if a.rebuild_layouts:
        rebuild_layouts()
        return
    data_dir = a.data
    if data_dir is None:
        sys.path.insert(0, os.path.join(HERE, '..', '..', 'coded'))
        from config import DATA_PATH                     # pylint: disable=import-outside-toplevel
        data_dir = str(DATA_PATH)
    sheets, notes = export(data_dir, a.out, a.countries, a.energy_year, a.csv_dir)
    for name, (_, rows) in sheets.items():
        print(f'{name}: {len(rows)} rows')
    for n in notes:
        print('note:', n)
    print(f'wrote {a.out}')


if __name__ == '__main__':
    main()
