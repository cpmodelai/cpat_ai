"""
Write every CSV of one Coded CPAT data version (e.g. data/dummy) into one Excel workbook, the data
source the Excel prototype links to (plan: CAVEATS.md (finished plan)).

    Index sheet         one row per table: sheet, source file, layout, rows, columns, countries, licence
                        class (proposed), MVP tab, MD5 of the source CSV
    README sheet        version, source, how to query one table for one country
    c_<file>            one sheet per CSV, the file as it is, as an Excel table named c_<file>
    L_<tab>             the legacy-layout tables the MVP loads directly (EnergyCons, Prices_dom, HHSurvey,
                        IO_GTAP, built as export_to_legacy.py does; v0.7.1: WEO, GDPRatios, HH_Elast, UNPop, built by
                        the converters of convert_data_workbook.py; Balances, the MVP's own Egypt table), one
                        header row (the code row)

Every table has a header in row 1, data from row 2, and, where it has a country column, a last column
FilterISO3 (upper-case ISO code) so that every query filters the same way. Header cells are made unique
(case-insensitive, as Excel requires: "iso3" and "ISO3" clash) and non-blank; the Index lists any header that
was changed. The finished file is checked with excel_ai/shared/excel_lint.py (NORMS.md section 3g).

Run from data/:
    python scripts/build_data_workbook.py                     # dummy -> workbooks/CPAT_Data_dummy_python.xlsx
    python scripts/build_data_workbook.py --data /path/real --version real --out /path/CPAT_Data_real_python.xlsx
Only the dummy workbook is committed; the real data stay outside the repository. This is the Python format;
scripts/convert_data_workbook.py converts it to the CPAT (legacy) format and back.
"""
import argparse
import csv
import datetime
import hashlib
import os
import re
import sys

import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import export_to_legacy as ex  # noqa: E402

DATA_ROOT = os.path.normpath(os.path.join(HERE, '..'))         # data/
REPO = os.path.dirname(DATA_ROOT)
BALANCES_CSV = os.path.join(DATA_ROOT, 'mvp_legacy_extracts', 'legacy_Balances.csv')

# Proposed classes, from the tables legacy strips in its NoPropData file (Balances, EnergyCons, Prices_dom, EF_PM,
# IO_GTAP, HHSurvey, ASPIRE, WHOCooking, CalVal, Tran_Scatter). To be confirmed by the CPAT team.
PROPRIETARY = {'energy_consumption', 'prices_dom', 'distn_hh_survey', 'distn_io_gtap', 'distn_aspire',
               'distn_who_cooking', 'cal_val', 'L_EnergyCons', 'L_Prices_dom', 'L_HHSurvey', 'L_IO_GTAP', 'L_Balances'}
TO_CHECK = {'air_data', 'distn_hh_elast', 'co_benefits_ffs', 'ic'}
# The MVP data tab each table feeds (proposed; c_ tables need converting to the MVP layout first).
MVP_TAB = {
    'weo': 'WEO', 'wdi': 'WEO (deflators)', 'distn_gdp_ratios': 'GDPRatios', 'distn_hh_elast': 'HH_Elast',
    'ghgs': 'GHGs', 'ghg_adjustments': 'GHGs (2023-24 shocks)', 'ch4_inputs': 'CH4Inputs', 'un_pop': 'UNPop',
    'ef_ghg': 'EF_GHG', 'co2_efs_global': 'EF_GHG', 'oil_product_shares': 'OilProductShares',
    'elasticities': 'Elasticities', 'prices_int': 'Prices_int', 'existing_ct': 'ECP', 'existing_ets_nat': 'ECP',
    'existing_ets_reg': 'ECP', 'do_ct_ets_exist': 'ECP', 'mpp': 'Power', 'lcoe_tmp': 'Power',
    'energy_consumption': 'EnergyCons', 'prices_dom': 'Prices_dom', 'distn_hh_survey': 'HHSurvey',
    'distn_io_gtap': 'IO_GTAP', 'distn_aspire': 'ASPIRE', 'distn_who_cooking': 'WHOCooking',
    'distn_mapping_countries_to_gtap10': 'DistMapping', 'distn_mapping_sector_crosswalk': 'DistMapping',
    'L_EnergyCons': 'EnergyCons', 'L_Prices_dom': 'Prices_dom', 'L_HHSurvey': 'HHSurvey', 'L_IO_GTAP': 'IO_GTAP',
    'L_Balances': 'Balances'}
# v0.7.1: Coded CPAT table -> L_ table in the legacy layout, through the converters of convert_data_workbook.py
LEGACY_CONVERTED = {'weo': 'L_WEO', 'distn_gdp_ratios': 'L_GDPRatios', 'distn_hh_elast': 'L_HH_Elast',
                    'un_pop': 'L_UNPop'}
L_SOURCE = {'L_EnergyCons': 'energy_consumption.csv', 'L_Prices_dom': 'prices_dom.csv',
            'L_HHSurvey': 'distn_hh_survey.csv', 'L_IO_GTAP': 'distn_io_gtap.csv',
            'L_Balances': 'MVP data/legacy_Balances.csv', 'L_WEO': 'weo.csv', 'L_GDPRatios': 'distn_gdp_ratios.csv',
            'L_HH_Elast': 'distn_hh_elast.csv', 'L_UNPop': 'un_pop.csv'}
COUNTRY_COLS = ['CountryCode', 'Country Code', 'ISO-3 Country Code', 'iso3', 'countrycode', 'country_code', 'ISO']
NUM = re.compile(r'^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$')
HEAD = Font(bold=True, color='FFFFFF')
FILL = PatternFill('solid', fgColor='1F4E78')
FILTER_COL = 'FilterISO3'      # must not equal any source header, case-insensitively


def _val(s):
    """CSV text -> number where it is one (codes with leading zeros stay text)."""
    s = s.strip()
    if s == '':
        return None
    if NUM.match(s) and not (len(s) > 1 and s[0] == '0' and s[1].isdigit()):
        f = float(s)
        return int(f) if re.fullmatch(r'[+-]?\d+', s) and abs(f) < 1e15 else f
    return s


def _unique(header):
    """Excel tables need unique, non-blank header text. Returns the header and the changes made."""
    out, seen, changed = [], set(), []
    for i, h in enumerate(header, 1):
        h0 = '' if h is None else str(h).replace('﻿', '').replace('\n', ' ').strip()
        h1 = h0 or f'Column{i}'
        k, n = h1, 2
        while k.lower() in seen:
            k, n = f'{h1}_{n}', n + 1
        seen.add(k.lower())
        out.append(k)
        if k != h0:
            changed.append(f'{h0 or "(blank)"} -> {k}')
    return out, changed


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    if header and header[0] == '' and len(rows) > 1 and rows[1][:2] == ['Country', 'CountryCode']:
        # ghgs.csv: two header rows (sector, gas) -> one ("1. Energy | CO2")
        header = [f'{a} | {b}' if a else b for a, b in zip(rows[0], rows[1])]
        data = rows[2:]
    width = max(len(header), max((len(r) for r in data), default=0))
    header = header + [''] * (width - len(header))
    return header, [[_val(v) for v in r] + [None] * (width - len(r)) for r in data]


def _iso3(header, rows, name):
    """Add an upper-case FilterISO3 column for the country filter, if the table has a country column."""
    assert FILTER_COL.lower() not in {h.lower() for h in header}, name
    if name == 'L_EnergyCons':
        key = lambda r: str(r[0]).split('.')[0].upper()            # 'egy.mit.enc.ele'
    elif name == 'L_Prices_dom':
        i = header.index('countrycode')
        key = lambda r: r[i]
    else:
        col = next((c for c in COUNTRY_COLS if c in header), None)
        if col is None:
            return header, rows, ''
        i = header.index(col)
        key = lambda r: str(r[i]).upper() if r[i] is not None else None
        if not any(isinstance(r[i], str) and re.fullmatch(r'[A-Za-z]{3}', r[i]) for r in rows):
            return header, rows, ''
    return header + [FILTER_COL], [r + [key(r)] for r in rows], FILTER_COL


def _legacy_tables(data_dir):
    """The four legacy-layout tables, as export_to_legacy.py builds them; header = the code row."""
    lay = ex.load_layouts()
    out = {}
    for name, fn in (('L_EnergyCons', lambda l: ex.energy_cons_rows(data_dir, l, None, 2022)),
                     ('L_Prices_dom', lambda l: ex.prices_dom_rows(data_dir, l, None)),
                     ('L_HHSurvey', lambda l: ex.hh_survey_rows(data_dir, l, None)),
                     ('L_IO_GTAP', lambda l: ex.io_gtap_rows(data_dir, l, None))):
        l = lay[name[2:]]
        rows, notes = fn(l)
        out[name] = (list(l['header_rows'][-1]), [list(r) for r in rows], notes)
    # v0.7.1: tables the MVP keeps in the legacy layout, built by the CPAT-format converters (convert_data_workbook.py);
    # header = the legacy column-header row, which is the MVP header row 3
    import convert_data_workbook as cdw
    tables = cdw.read_python_tables(data_dir)
    layouts = cdw.load_layouts()
    for table, name in LEGACY_CONVERTED.items():
        if table not in tables:
            continue
        sheet, _keys, fwd, _back = cdw.CONVERTERS[table]
        layout = dict(layouts[sheet], sheet=sheet)
        rows, notes = fwd(tables, data_dir, layout)
        header = cdw._hdr(layout)
        out[name] = (header, cdw._padded([[cdw._py(v) for v in r] for r in rows], layout), notes)
    # Balances: no Coded CPAT dummy table yet; the MVP's own table (Egypt rows of the public legacy file) stands in,
    # so that a refresh of the MVP from this workbook gives its shipped results (format sample, not dummy values)
    path = os.path.join(BALANCES_CSV)
    if os.path.exists(path):
        header, rows = read_csv(path)
        out['L_Balances'] = (header, rows, ['Egypt rows of the MVP Balances tab (public legacy file), not dummy values'])
    return out


def _sheet_name(name, used):
    s = name[:31]
    n = 2
    while s.lower() in used:
        s, n = f'{name[:28]}_{n}', n + 1
    used.add(s.lower())
    return s


def _write_table(ws, tname, header, rows):
    ws.append(header)
    for r in rows:
        ws.append(r)
    for c in ws[1]:
        c.font, c.fill = HEAD, FILL
    ref = f'A1:{get_column_letter(len(header))}{len(rows) + 1}'
    t = Table(displayName=tname, ref=ref)
    t.tableStyleInfo = TableStyleInfo(name='TableStyleLight9', showRowStripes=True)
    ws.add_table(t)
    ws.freeze_panes = 'B2'


def build(data_dir, version, out_path, source=None):
    wb = openpyxl.Workbook()
    readme = wb.active
    readme.title = 'README'
    index = wb.create_sheet('Index')
    used = {'readme', 'index'}
    entries = []

    tables = []
    for fn in sorted(f for f in os.listdir(data_dir) if f.lower().endswith('.csv')):
        path = os.path.join(data_dir, fn)
        header, rows = read_csv(path)
        md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
        tables.append((os.path.splitext(fn)[0], 'c_', fn, header, rows, md5, 'coded (as the CSV)', []))
    for name, (header, rows, notes) in _legacy_tables(data_dir).items():
        tables.append((name, '', 'built from ' + L_SOURCE[name],
                       header, rows, '', 'MVP-ready (legacy table, code header row)', notes))

    for name, prefix, src, header, rows, md5, layout, notes in tables:
        tname = prefix + re.sub(r'\W', '_', name)
        header, changed = _unique(header)
        header, rows, ccol = _iso3(header, rows, name)
        countries = len({r[-1] for r in rows if r[-1]}) if ccol else ''
        ws = wb.create_sheet(_sheet_name(tname, used))
        _write_table(ws, tname, header, rows)
        lic = 'possibly proprietary' if name in PROPRIETARY else 'check' if name in TO_CHECK else 'public'
        entries.append([tname, ws.title, src, layout, len(rows), len(header), ccol or '(global)', countries,
                        lic, MVP_TAB.get(name, ''), md5, '; '.join(changed + notes)[:2000]])

    hdr = ['Table', 'Sheet', 'Source', 'Layout', 'Rows', 'Columns', 'Country filter column', 'Countries',
           'Licence class (proposed)', 'MVP tab (proposed)', 'MD5 of source CSV', 'Header changes and notes']
    _write_table(index, 'Index', hdr, entries)
    for col, w in zip('ABCDEFGHIJKL', (34, 31, 38, 34, 8, 8, 12, 10, 20, 22, 34, 80)):
        index.column_dimensions[col].width = w

    stamp = datetime.date.today().isoformat()
    lines = [
        ('CPAT data workbook', f'version: {version}'),
        ('Built', f'{stamp} by data/scripts/build_data_workbook.py'),
        ('Source', source or os.path.relpath(data_dir, REPO).replace(os.sep, '/') + '/ (one table per CSV)'),
        ('What it is', 'Every table of this data version, one Excel table per sheet, header in row 1. '
                       'The Excel prototype keeps its own copy of one country (Egypt) and can refresh selected '
                       'tables from this file with Power Query.'),
        ('Dummy data', 'Fake, non-proprietary values in the real formats. Never use them for analysis.'
                       if version == 'dummy' else ''),
        ('Index', 'One row per table: layout, size, country filter column, proposed licence class, the MVP tab it '
                  'feeds, MD5 of the source CSV.'),
        ('c_ tables', 'The Coded CPAT CSVs as they are. Their layout differs from the MVP tabs; they feed the MVP '
                      'after conversion (planned).'),
        ('L_ tables', 'Legacy-layout tables the MVP loads directly (code header row = the MVP header row 3).'),
        ('FilterISO3 column', 'Added as the last column of every table with a country column, so every query filters '
                        'the same way. Remove it after filtering.'),
        ('Power Query, one table, one country',
         'let Src = Excel.Workbook(Web.Contents("<file URL>"), true, true), '
         'T = Src{[Item="L_HHSurvey", Kind="Table"]}[Data], '
         'R = Table.RemoveColumns(Table.SelectRows(T, each [FilterISO3] = "EGY"), {"FilterISO3"}) in R'),
        ('Versions', 'dummy (this file, in the repository); dummy-proprietary (real public tables, dummy '
                     'proprietary tables); real (team only, on the restricted OneDrive/SharePoint site). Same '
                     'table names and columns in every version.'),
    ]
    for r, (a, b) in enumerate(lines, 1):
        readme.cell(r, 1, a).font = Font(bold=True)
        readme.cell(r, 2, b)
    readme.column_dimensions['A'].width = 34
    readme.column_dimensions['B'].width = 140
    # README, Index, then the MVP-ready L_ tables, then the c_ tables
    order = {'README': 0, 'Index': 1}
    pos = {s.title: i for i, s in enumerate(wb._sheets)}
    wb._sheets.sort(key=lambda s: (order.get(s.title, 2 if s.title.startswith('L_') else 3), pos[s.title]))
    wb.save(out_path)
    sys.path.insert(0, os.path.join(REPO, 'excel_ai', 'shared'))
    import excel_lint
    problems = excel_lint.lint(out_path)
    if problems:
        raise SystemExit(f'{out_path}: Excel would repair it:\n  ' + '\n  '.join(problems))
    return entries


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--data', default=os.path.join(DATA_ROOT, 'dummy'), help='folder of CSVs')
    ap.add_argument('--version', default='dummy', help='version name (dummy, dummy-proprietary, real)')
    ap.add_argument('--out', help='output workbook (default: data/workbooks/CPAT_Data_<version>_python.xlsx)')
    a = ap.parse_args(argv)
    out = a.out or os.path.join(DATA_ROOT, 'workbooks', f'CPAT_Data_{a.version}_python.xlsx')
    entries = build(a.data, a.version, out)
    print(f'{out}: {len(entries)} tables, {sum(e[4] for e in entries)} rows')


if __name__ == '__main__':
    main()
