"""Write data/catalog.csv: the generic catalogue of every data table, the same for every edition (data/README.md).

One row per tidy table (from the specs, data/scripts/tidy_specs.py), then one per data tab of the legacy workbook that
has no tidy table yet, then one per entry of the legacy "Data sources" tab that names no tab of the workbook. Each
edition's data_sources.csv is this catalogue plus the edition's column values (data/scripts/build_edition.py). Columns:

    tidy_file            the tidy CSV in <edition>/tidy/ (blank: not in tidy yet)
    excel_tab            the tab in <edition>/legacy_xlsx/CPAT_LegacyData.xlsx (= the legacy tab name; blank: no tab)
    proprietary          proprietary / non-proprietary: proprietary only for the six confirmed tabs (PROPRIETARY)
    provenance           where the table comes from (legacy version and place, or how it was derived)
    status               tidy + xlsx / legacy 465 only (not in tidy yet) / Data sources entry only (no tab)
                         (tables kept as they are have their own sheet, e.g. xai_weo, ap459_gbd: not a legacy tab)
    data_sources_entry   the name in the legacy "Data sources" tab (column C) the source columns come from
    module, topic, data_category, data_source, link, legacy_notes    the legacy "Data sources" tab, as it is

Run from the repository root (needs pyxlsb):
    python data/scripts/build_catalog.py
"""
import csv
import os
import sys

from pyxlsb import open_workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import editions as ED  # noqa: E402
from tidy_specs import ASIS, CELLS, TABLES  # noqa: E402

LEGACY = ED.SHELL                                  # the "Data sources" tab and the tab list
OUT = os.path.join(ED.DATA, 'catalog.csv')

# The confirmed proprietary tabs (user 2026-10-30); every other table is non-proprietary.
PROPRIETARY = {'Balances', 'EnergyCons', 'Prices_dom', 'HHSurvey', 'IO_GTAP', 'Tran_Scatter'}

# Legacy tabs that hold no input data: not listed.
NOT_DATA = {'Data sources', 'MTOutputs', 'Glossary', 'Notes', 'VersionTracker'}

# "Data sources" entry (column C) -> the tabs it describes; an entry not here and not a tab gets its own row.
DS_TABS = {
    'Prices': ['Prices_dom'], 'ECPPC': ['ECP', 'ETS+LTS'], 'EnergyConsumption': ['EnergyCons'],
    'WEO2020': ['WEO'], 'WEOBOP': ['WEO'], 'Energy_intprice': ['Prices_int'], 'Popn': ['UNPop'],
    'IEABalances': ['Balances'], 'HHPrice_Elasticities': ['HH_Elast'],
    'Tran': ['Transport1', 'Transport2', 'Transport3'], 'Air_1': ['WB', 'ILO', 'IHME'], 'Air_2': ['GBD'],
    'iF PP': ['IF PP'],
}

# Provenance of the tidy tables whose source is not simply the legacy 465 tab of the same name (by legacy source
# file, data/Public01/tidy/_manifest.csv column legacy_source).
PROVENANCE = {
    'legacy_Balances.csv': 'legacy 465 NoPropData, Balances rows 13+ (Egypt rows in the public file)',
    'legacy_Tran_Scatter.csv': 'legacy 465 NoPropData, Tran_Scatter (Egypt rows; IRF World Road Statistics)',
    'legacy_EnergyCons.csv': 'derived from Balances (Excel-AI extract_legacy_tables.py)',
    'prices_dom.csv': 'legacy Prices_dom in the 99-column Excel-AI layout (Egypt only)',
    'prices_dom_changes.csv': 'Egypt corrections over Prices_dom (user 2026-10-09); derived from Prices_dom',
    'legacy_HHSurvey.csv': 'legacy 456 NoPropData, HHSurvey',
    'legacy_HH_Elast.csv': 'legacy 456 NoPropData, HH_Elast',
    'legacy_IO_GTAP.csv': 'legacy 465 NoPropData, IO_GTAP (cut to Egypt)',
    'legacy_ASPIRE.csv': 'legacy 465 NoPropData, ASPIRE (cut to Egypt)',
    'legacy_WHOCooking.csv': 'legacy 465 NoPropData, WHOCooking (cut to Egypt)',
    'legacy_GHGHist.csv': 'legacy 465 NoPropData, GHGs rows 954-1189',
    'transport_params.csv': 'legacy 465, Dashboard rows 61-98 and 540-559, Mitigation rows 4304-4332',
    'transport_paths.csv': 'legacy 465 (Egypt run), Mitigation rows 2051, 2095, 2122, 2170; Manual inputs 375-377',
    'fuel_units.csv': 'legacy 465, Mitigation rows 980-1009 (GJ per price unit)',
    'distn_catmap.csv': 'legacy 465, Distribution C.I rows 668-736',
    'distn_programs.csv': 'legacy 465, Distribution rows 184-210',
    'distn_gtapmap.csv': 'legacy 465, Distribution D.VI',
    'distn_passthrough.csv': 'legacy 465, Distribution I470:I486',
    'range_anxiety_fit.csv': 'fitted on the Excel-AI 0.9.0 road model (scenario 1, 2025), a run that used Balances '
                             'and Prices_dom',
    'module_FromAirPollution_cells.csv': 'Excel-AI tab FromAirPollution: typed module values (Egypt, legacy 465 run)',
    'module_FromTransportCB_cells.csv': 'Excel-AI tab FromTransportCB: typed module values',
    'cooking_fuel.csv': 'derived from HHSurvey and WHOCooking (Excel-AI extract_cooking.py): most-used cooking fuel '
                        'and the decile shares of its spend, the only household data Mitigation reads (1.2.2)',
}

# The legacy 459 air-pollution tables kept as they are (tidy ap459_<name>) -> their legacy tab.
AP459_TABS = {'ap459_wb': 'WB', 'ap459_gbd': 'GBD', 'ap459_ihme': 'IHME', 'ap459_ilo': 'ILO',
              'ap459_exposure_coefs': 'ExposureCoefs', 'ap459_if_pp': 'IF PP', 'ap459_conc_mat': 'ConcMat',
              'ap459_air_data': 'Air_Data', 'ap459_air_meta': 'Air_meta'}

HEADER = ['tidy_file', 'excel_tab', 'proprietary', 'provenance', 'status', 'data_sources_entry', 'module', 'topic',
          'data_category', 'data_source', 'link', 'legacy_notes']


def read_legacy():
    """(tab names after DATA_MITIGATION->, Data sources entries as dicts)."""
    with open_workbook(LEGACY) as wb:
        sheets = wb.sheets
        with wb.get_sheet('Data sources') as s:
            rows = [{c.c: c.v for c in r if c.v not in (None, '')} for r in s.rows()]
    tabs = [t for t in sheets[sheets.index('DATA_MITIGATION->'):] if not t.endswith('->') and t not in NOT_DATA]
    entries = []
    for r in rows[5:]:                           # header on row 5
        if 3 not in r:
            continue
        entries.append(dict(data_sources_entry=str(r[3]).strip(), module=r.get(1, ''), topic=str(r.get(2, '')).strip(),
                            data_category=r.get(4, ''), data_source=r.get(6, ''), link=r.get(7, ''),
                            legacy_notes=r.get(8, '')))
    return tabs, entries


def sources_by_tab(tabs, entries):
    """{tab: merged Data sources columns}, and the entries that name no tab."""
    by_tab, orphans = {}, []
    for e in entries:
        targets = DS_TABS.get(e['data_sources_entry']) or ([e['data_sources_entry']]
                                                           if e['data_sources_entry'] in tabs else [])
        if not targets:
            orphans.append(e)
        for t in targets:
            if t in by_tab:                      # two entries on one tab (WEO2020, WEOBOP): join them
                by_tab[t] = {k: ' | '.join(x for x in (by_tab[t][k], e[k]) if x) for k in e}
            else:
                by_tab[t] = dict(e)
    return by_tab, orphans


def main():
    tabs, entries = read_legacy()
    by_tab, orphans = sources_by_tab(tabs, entries)
    manifest = ([dict(table=sp['tidy'], legacy_source=f, kind='table', legacy_tab=sp['sheet']) for f, sp in TABLES.items()]
                + [dict(table=b['name'], legacy_source=f, kind='cells block', legacy_tab=sp['sheet'])
                   for f, sp in CELLS.items() for b in sp.get('blocks', [])]
                + [dict(table=sp['tidy'], legacy_source=f, kind='as is', legacy_tab=sp['sheet']) for f, sp in ASIS.items()])
    manifest.sort(key=lambda r: r['table'])
    out = []
    for r in manifest:
        tab = r['legacy_tab']
        if r['kind'] == 'as is' and r['table'].startswith('ap459_'):
            src = AP459_TABS.get(r['table'], '')
            prov = (f'legacy 459 NoPropData, tab {src} (air pollution), kept as extracted' if src else
                    'legacy 459 NoPropData: list of the air-pollution extracts')
        elif r['kind'] == 'as is':
            src = ''
            prov = PROVENANCE.get(r['legacy_source'],
                                  f"Excel-AI table {r['legacy_source']} (written by the extract scripts in excel_ai/"
                                  'mitigation/ from the legacy workbook, or by the Excel-AI checks), kept as it is')
        else:
            src = tab
            prov = PROVENANCE.get(r['legacy_source'], f'legacy 465 NoPropData, {tab}')
        out.append(dict(tidy_file=r['table'] + '.csv', excel_tab=tab, provenance=prov, status='tidy + xlsx',
                        **by_tab.get(src, {})))
    in_tidy = {r['legacy_tab'] for r in manifest}
    for tab in tabs:
        if tab not in in_tidy:
            out.append(dict(tidy_file='', excel_tab=tab, provenance=f'legacy 465 NoPropData, {tab}',
                            status='legacy 465 only (not in tidy yet)', **by_tab.get(tab, {})))
    for e in orphans:
        out.append(dict(tidy_file='', excel_tab='', provenance='legacy 465 Data sources tab',
                        status='Data sources entry only (no tab)', **e))
    for r in out:
        r['proprietary'] = 'proprietary' if r['excel_tab'] in PROPRIETARY else 'non-proprietary'
        for k in HEADER:
            r[k] = ' '.join(str(r.get(k, '')).split())      # one line per cell (the legacy text has line breaks)
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, HEADER, lineterminator='\n')
        w.writeheader()
        w.writerows(out)
    n = sum(r['proprietary'] == 'proprietary' for r in out)
    print(f'{len(out)} rows ({n} proprietary) written to {OUT}')


if __name__ == '__main__':
    main()
