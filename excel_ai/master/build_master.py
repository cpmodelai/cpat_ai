"""CPAT-AI Master workbook (user 2026-10-31, v1.2.0): the user guide of the CPAT-AI workbooks and the only workbook with
macros. It lists the modules (version, where the latest unactivated .xlsx is, locally and on GitHub, and the activated
.xlsb it writes in active_workbooks), activates them, updates their data tables and the distribution inputs, and
stores scenario results as values (StoredScenarios, ten slots, MTOutputs' rows) with their comparison (CompareStored).

    python build_master.py      # master/releases/CPAT-AI-Master_UserGuide_v<version>.xlsm and its copy
                                # active_workbooks/CPAT-AI-Master_UserGuide.xlsm (after the mitigation build: it
                                # reads mitigation/stored_scenarios.csv for the stored slots)
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import csv
import os
import re
import shutil
import tempfile

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

import build as P                                   # noqa: E402  the mitigation builder (layout, styles, helpers)

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = P.VERSION                                 # the Master carries the version of the release
NAME = 'CPAT-AI-Master_UserGuide'
OUT = P.REL.versioned(NAME, VERSION, 'xlsm')         # master/releases/<name>_v<version>.xlsm
ACTIVE_COPY = os.path.join(P.REL.ACTIVE, f'{NAME}.xlsm')   # what people open (active_workbooks)
BAS = os.path.join(HERE, 'CPATMaster.bas')
REPO_RAW = 'https://github.com/cpmodelai/cpat_ai/raw/main/excel_ai'   # the unactivated .xlsx of each module
SS_SLOTS = 10                                       # stored scenario slots (user 2026-10-31)
ZOOM = P.ZOOM


def module_version(path, pattern):
    m = re.search(pattern, open(path, encoding='utf-8').read(), re.M)
    return m.group(1)


MODULES = [  # module, version, unactivated file (relative to excel_ai), sheets filled on activation
    ('Mitigation', P.VERSION, os.path.relpath(P.LATEST, P.REL.XL).replace(os.sep, '/'), 'Mitigation,MTOutputs'),
    ('Distribution', module_version(os.path.join(P.REL.XL, 'distribution', 'build_distribution.py'),
                                    r"^VERSION = '([^']+)'"),
     os.path.relpath(P.REL.permalink('CPAT-AI-Distribution-Prototype', 'xlsx'), P.REL.XL).replace(os.sep, '/'), ''),
    ('Air pollution', module_version(os.path.join(P.REL.XL, 'air_pollution', 'build_workbook.py'), r'^VERSION = "([^"]+)"'),
     os.path.relpath(P.REL.permalink('CPAT-AI-Air-Pollution-Standalone', 'xlsx'), P.REL.XL).replace(os.sep, '/'), '')]
MOD_HEAD = ['Module', 'Latest version', 'Unactivated workbook (.xlsx, in the repository, relative to excel_ai)',
            'GitHub link (the same file)', 'Activated workbook (.xlsb, next to this workbook)',
            'Filled on activation (sheets)', 'Last activated (here)']
COL_FILE, COL_URL, COL_ACT, COL_FILL, COL_LAST = 3, 4, 5, 6, 7
BUTTONS = [('Activate all modules', 'ActivateAll'), ('Activate Mitigation', 'ActivateMitigation'),
           ('Activate Distribution', 'ActivateDistribution'), ('Activate Air pollution', 'ActivateAirPollution'),
           ('Update data tables', 'UpdateDataTables'), ('Update Distribution from Mitigation',
                                                        'UpdateDistributionFromMitigation'),
           ('Store live scenarios', 'StoreLiveScenarios'), ('Run stored scenarios', 'RunStoredScenarios'),
           ('Clear stored scenarios', 'ClearStoredScenarios')]
BTN_ROW0, BTN_COL0 = 4, 4                           # 0-based anchors: right of the guide text
VERSION_LOG = [('1.2.0', '2026-10-31', 'First version (user 2026-10-31): user guide, module table, activation (fill '
                                       f'{P.SHIP_LAST_YEAR} across to {P.LAST_YEAR}, recalculate, save as .xlsb), '
                                       'every macro of CPAT-AI (data tables, distribution from mitigation, batch runs), '
                                       'stored scenarios (ten slots) and their comparison.')]


def bar(ws, row, text, width, fill_, font):
    P.bar(ws, row, text, width, fill_, font)


def build_guide(wb):
    ws = wb.active
    ws.title = 'UserGuide'
    w = 7
    bar(ws, 2, f'{NAME} v{VERSION}: the user guide of the CPAT-AI workbooks, and their macros', w, P.F_TITLE, P.FONT_T)
    P.put(ws, 'A3', 'The Climate Policy Assessment Tool in Excel (CPAT-AI): one workbook per module, without macros; '
                    'this Master opens them, activates them, feeds them and stores their results. Buttons on the right.')
    r = 5
    bar(ws, r, 'How to use it', 3, P.F_BAND, P.FONT_SUBBAR)
    steps = [
        'Keep this workbook in excel_ai/active_workbooks of the repository (git clone or the SyncRepo script); the '
        'modules are then found locally, else downloaded from GitHub (the links below).',
        f'Activate: the module\'s .xlsx ships with formulas to {P.SHIP_LAST_YEAR} (smaller, faster to open). Activation '
        f'copies the {P.SHIP_LAST_YEAR} column across to {P.LAST_YEAR}, recalculates and saves the module as .xlsb next '
        'to this workbook. Work in the .xlsb.',
        'Scenarios: in the mitigation workbook, MTInputs (ScenarioDefinition): J = baseline, K = the live policy '
        'scenario, L onwards = definitions (Run? = Yes for the batch run). Results: MTOutputs (scenarios side by '
        'side) and ScenarioCompare. F9 recalculates.',
        'Data: choose the data source and the rows (one country or all countries) on tab Settings, then Update '
        'data tables (Power Query; the mitigation workbook keeps the source on its tab FromMaster).',
        'Distribution: Update Distribution from Mitigation copies the exports of Mitigation (section 19a) into the '
        'distribution workbook.',
        'Store: Store live scenarios copies the scenario groups of MTOutputs into StoredScenarios (values); Run '
        'stored scenarios runs every definition through the live column and stores each. CompareStored compares '
        'the stored scenarios.']
    for k, s in enumerate(steps, r + 1):
        P.put(ws, f'A{k}', f'{k - r}.', P.FONT_B)
        c = P.put(ws, f'B{k}', s)
        c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[k].height = 42
    r += len(steps) + 2
    bar(ws, r, 'The modules: latest version and where to find them', w, P.F_BAND, P.FONT_SUBBAR)
    for j, h in enumerate(MOD_HEAD, 1):
        P.put(ws, f'{P.L(j)}{r + 1}', h, P.FONT_B).border = Border(bottom=P.THIN)
    for k, (mod, ver, rel, fill_) in enumerate(MODULES, r + 2):
        url = f'{REPO_RAW}/{rel}'
        act = os.path.basename(rel).replace('.xlsx', '.xlsb')
        for j, v in enumerate([mod, ver, rel, url, act, fill_, ''], 1):
            c = P.put(ws, f'{P.L(j)}{k}', v)
            if j == COL_URL:
                c.hyperlink = url
                c.style = 'Hyperlink'
    wb.defined_names['ModTable'] = DefinedName('ModTable', attr_text=f'UserGuide!$A${r + 2}:$G${r + 1 + len(MODULES)}')
    r += len(MODULES) + 3
    bar(ws, r, 'Storage (NORMS 5a)', 3, P.F_BAND, P.FONT_SUBBAR)
    for k, s in enumerate([
            'excel_ai/<module>/<name>_latest.xlsx: the latest unactivated module (built by its builder; versions in '
            '<module>/releases/).',
            'excel_ai/active_workbooks/: this Master (.xlsm) and the activated modules (<name>_latest.xlsb). The .xlsb '
            'are generated files: on a git conflict take either side and activate again; never merge them.'], r + 1):
        P.put(ws, f'B{k}', s)
    r += 4
    bar(ws, r, 'Version log', 3, P.F_BAND, P.FONT_SUBBAR)
    for k, (v, d, s) in enumerate(VERSION_LOG, r + 1):
        P.put(ws, f'A{k}', v)
        P.put(ws, f'B{k}', s).alignment = Alignment(wrap_text=True, vertical='top')
        P.put(ws, f'C{k}', d)
    for col, wd in {'A': 16, 'B': 90, 'C': 46, 'D': 70, 'E': 42, 'F': 22, 'G': 18}.items():
        ws.column_dimensions[col].width = wd
    ws.sheet_view.zoomScale = ZOOM
    ws.sheet_properties.tabColor = P.F_TABDIV
    return ws


def build_settings(wb):
    ws = wb.create_sheet('Settings')
    bar(ws, 2, 'Settings: the data source of the linked data tables of the modules', 8, P.F_TITLE, P.FONT_T)
    P.put(ws, 'A3', 'Update data tables (UserGuide) loads the linked tabs of the activated mitigation workbook from '
                    'this source and writes it on the module\'s tab FromMaster.', P.FONT)
    srcs = P.DATA_SOURCES
    rows_ = [(5, 'Data source', srcs[0][0], f'=$F$5:$F${4 + len(srcs)}'),
             (6, 'Rows to load', 'Country', '"Country,All countries"')]
    for r, lab, v, lst in rows_:
        P.put(ws, f'B{r}', lab, P.FONT_B)
        P.put(ws, f'C{r}', v, P.FONT_B, P.F_INPUT)
        dv = DataValidation(type='list', formula1=lst, allow_blank=False)
        ws.add_data_validation(dv)
        dv.add(f'C{r}')
    P.put(ws, 'D6', 'Country: the rows of the country of the module (MTInputs, Model settings); All countries: every '
                    'row of every linked table (larger, slower)', P.FONT_NOTE)
    P.put(ws, 'F4', 'Source', P.FONT_B)
    P.put(ws, 'G4', 'Kind', P.FONT_B)
    P.put(ws, 'H4', 'Path or URL (file: blank = CPAT_LegacyData.xlsx in <repo>/data/Public01/legacy_xlsx/; web: the raw '
                    'file address; SharePoint: File > Info > Copy path)', P.FONT_B)
    for k, (nm, kind, loc) in enumerate(srcs, 5):
        P.put(ws, f'F{k}', nm)
        P.put(ws, f'G{k}', kind)
        P.put(ws, f'H{k}', loc, P.FONT, P.F_INPUT if kind != 'none' else None)
    for nm, ref in (('DataSource', '$C$5'), ('DataRows', '$C$6'), ('DataSrcTable', f'$F$5:$H${4 + len(srcs)}')):
        wb.defined_names[nm] = DefinedName(nm, attr_text=f'Settings!{ref}')
    for col, wd in {'A': 4, 'B': 16, 'C': 40, 'D': 4, 'E': 4, 'F': 40, 'G': 8, 'H': 100}.items():
        ws.column_dimensions[col].width = wd
    ws.sheet_view.zoomScale = ZOOM
    ws.sheet_properties.tabColor = '92D050'


def slot_col(k):
    return P.COL_G0 + (k - 1) * P.GW


def stored_rows():
    """{scenario ID: (name, {stem: (description, unit, [values])})} of the build's batch run (stored_scenarios.csv)."""
    out = {}
    if not os.path.exists(P.STORED_CSV):
        return out
    with open(P.STORED_CSV, encoding='utf-8') as f:
        rd = csv.reader(f)
        next(rd)
        for row in rd:
            sid, name, stem, _code, desc, unit, _st = row[:7]
            vals = [float(v) if re.fullmatch(r'-?[\d.]+(?:e[-+]?\d+)?', v or '') else (v or None) for v in row[7:]]
            out.setdefault(int(sid), (name, {}))[1][stem] = (desc, unit, vals)
    return out


SS_ROW_NAME, SS_ROW_ID, SS_ROW_META = 4, 5, 6


def build_stored(wb):
    """StoredScenarios: the rows of MTOutputs (the same row numbers, so a group is copied in one block), ten slots in
    the columns of Mitigation's scenario groups; values only. Filled by the build with the baseline and the
    definitions of its batch run (Python emulation of RunAllScenarios)."""
    ws = wb.create_sheet('StoredScenarios')
    last = slot_col(SS_SLOTS) + P.NY + 1
    bar(ws, 2, 'StoredScenarios: scenario results stored as values (the rows of MTOutputs; one slot per scenario)', last,
        P.F_TITLE, P.FONT_T)
    P.put(ws, 'A3', 'Values only. Store live scenarios and Run stored scenarios (UserGuide) write the slots; row 5 '
                    'the scenario ID, row 4 its name, row 6 when and from which file. CompareStored compares them.')
    for j, h in enumerate(P.MTO_HEAD, 1):
        if h and j != 10:
            P.put(ws, f'{P.L(j)}1', h, P.FONT_B)
    P.put(ws, 'H4', 'Scenario name', P.FONT_B)
    P.put(ws, 'H5', 'Scenario ID', P.FONT_B)
    P.put(ws, 'H6', 'Stored', P.FONT_B)
    stored = stored_rows()
    ids = sorted(stored)[:SS_SLOTS]
    desc = {stem: (d, u) for _n, rows in stored.values() for stem, (d, u, _v) in rows.items()}
    for k in range(1, SS_SLOTS + 1):
        c0 = slot_col(k)
        P.put(ws, f'{P.L(c0)}1', f'Slot {k}: output code', P.FONT_B)
        for y in range(P.NY):
            P.put(ws, f'{P.L(c0 + 1 + y)}1', P.BASE_YEAR + y, P.FONT_B, P.F_BASE if y == 0 else None, '0')
    for i, (kind, it) in enumerate(P.MTO_ITEMS):
        r = P.mto_row(i)
        if kind == 'section':
            P.band(ws, r, it, last)
            continue
        stem = f"{it['tab']}.{it['var']}" if it['var'] else None
        live = it['var'] and it['tab'] == 'mit'
        P.put(ws, f'A{r}', stem, P.FONT_CODE_IT if live else P.FONT_NOTE)
        P.put(ws, f'B{r}', it['tab'] or '', P.FONT)
        P.put(ws, f'C{r}', it['legacy_body'] or None, P.FONT_CODE_IT)
        d, u = desc.get(stem, (it['indicator'] or it['var'], it['unit']))
        P.put(ws, f'H{r}', d, P.FONT if live else P.FONT_NOTE)
        P.put(ws, f'I{r}', u, P.FONT if live else P.FONT_NOTE)
    for k, sid in enumerate(ids, 1):
        c0 = slot_col(k)
        name, rows = stored[sid]
        P.put(ws, f'{P.L(c0 + 1)}{SS_ROW_NAME}', name, P.FONT_B)
        for c in range(c0, c0 + P.NY + 1):
            P.put(ws, f'{P.L(c)}{SS_ROW_ID}', sid, P.FONT_B, None, '0')
        P.put(ws, f'{P.L(c0 + 1)}{SS_ROW_META}', f'stored by the build of mitigation v{P.VERSION} (Python emulation of '
                                                 f'the batch run), {P.COUNTRY}', P.FONT_NOTE)
        for i, (kind, it) in enumerate(P.MTO_ITEMS):
            stem = f"{it['tab']}.{it['var']}" if kind == 'row' and it['var'] else None
            if stem not in rows:
                continue
            r = P.mto_row(i)
            P.put(ws, f'{P.L(c0)}{r}', f'{P.COUNTRY.lower()}.{stem}.{sid}', P.FONT_CODE_IT, P.F_CODE)
            for y, v in enumerate(rows[stem][2]):
                P.put(ws, f'{P.L(c0 + 1 + y)}{r}', v, P.FONT, None, it['fmt'])
    ws.freeze_panes = f'{P.L(P.COL_G0 + 1)}7'
    for col, wd in {'A': 26, 'B': 7, 'C': 22, 'D': 4, 'E': 4, 'F': 4, 'G': 4, 'H': 52, 'I': 14, 'J': 4}.items():
        ws.column_dimensions[col].width = wd
    for k in range(1, SS_SLOTS + 1):
        ws.column_dimensions[P.L(slot_col(k))].width = 26
        for y in range(P.NY):
            ws.column_dimensions[P.L(slot_col(k) + 1 + y)].width = 9
        ws.column_dimensions[P.L(slot_col(k) + P.NY + 1)].width = 3
    ws.sheet_view.zoomScale = ZOOM
    ws.sheet_properties.tabColor = '00AE49'
    g_last = P.L(last)
    for nm, ref in (('SSAll', f'$A$1:${g_last}${P.MTO_LAST}'), ('SSStem', f'$A$1:$A${P.MTO_LAST}'),
                    ('SSUnit', f'$I$1:$I${P.MTO_LAST}'), ('SSDesc', f'$H$1:$H${P.MTO_LAST}'),
                    ('SSScen', f'$A$5:${g_last}$5'), ('SSName', f'$A$4:${g_last}$4'),
                    ('SCYear', f'${P.L(P.COL_G0 + 1)}$1:${P.L(P.COL_G0 + P.NY)}$1')):
        wb.defined_names[nm] = DefinedName(nm, attr_text=f'StoredScenarios!{ref}')
    return ids


CS_R_YEAR, CS_R_YC, CS_R_COL = 5, 10, 11
CS_R_ID, CS_R_SHORT, CS_R_NAME = 13, 14, 15
CS_KEY_R0 = 18
CS_C0 = 4
CS_TS_R0 = CS_KEY_R0 + 3 * len(P.SC_KEY) + 2
CS_TS_H = SS_SLOTS + 7
CS_Y1 = CS_C0 + P.NY - 1


def build_compare(wb):
    """CompareStored: the stored scenarios against the first slot (the baseline), as ScenarioCompare in the module
    compares the live ones: the year, a key table (level, difference and % difference), time series with their line
    chart (the indicator of each block: the dropdown in its title)."""
    from openpyxl.chart import LineChart, Reference, Series
    from openpyxl.chart.series import SeriesLabel
    from openpyxl.chart.data_source import StrRef
    ws = wb.create_sheet('CompareStored')
    last = CS_Y1 + 12
    bar(ws, 2, 'CompareStored: the stored scenarios against the first slot (the baseline)', last, P.F_TITLE, P.FONT_T)
    P.put(ws, 'A3', 'Reads StoredScenarios (values). Choose the year; F9 recalculates. Indicator of each time series: '
                    'the dropdown in its title.')
    P.put(ws, f'B{CS_R_YEAR}', 'Year', P.FONT_B)
    P.put(ws, f'C{CS_R_YEAR}', P.SC_YEAR, P.FONT_B, P.F_INPUT, '0')
    dv = DataValidation(type='list', formula1='"' + ','.join(str(P.BASE_YEAR + k) for k in range(P.NY)) + '"')
    ws.add_data_validation(dv)
    dv.add(f'C{CS_R_YEAR}')
    P.put(ws, f'B{CS_R_YC}', 'Position of the year in a slot', P.FONT_HELP)
    P.put(ws, f'C{CS_R_YC}', f'=MATCH($C${CS_R_YEAR},SCYear,0)', P.FONT_HELP, None, '0')
    P.put(ws, f'B{CS_R_COL}', 'Column of the slot on StoredScenarios', P.FONT_HELP)
    P.put(ws, f'C{CS_R_ID}', 'Scenario ID', P.FONT_B)
    P.put(ws, f'C{CS_R_SHORT}', 'Slot', P.FONT_B)
    P.put(ws, f'C{CS_R_NAME}', 'Scenario', P.FONT_B)
    for k in range(SS_SLOTS):
        cl = P.L(CS_C0 + k)
        P.put(ws, f'{cl}{CS_R_COL}', slot_col(k + 1), P.FONT_HELP, None, '0')
        P.put(ws, f'{cl}{CS_R_ID}', f'=IF(INDEX(SSScen,{cl}${CS_R_COL})="","",INDEX(SSScen,{cl}${CS_R_COL}))', P.FONT_B,
              P.F_BASE if k == 0 else None, '0;-0;;@')
        P.put(ws, f'{cl}{CS_R_SHORT}', f'=IF({cl}${CS_R_ID}="","","S{k + 1}: "&{cl}${CS_R_ID})', P.FONT_B,
              P.F_BASE if k == 0 else None)
        P.put(ws, f'{cl}{CS_R_NAME}', f'=IF({cl}${CS_R_ID}="","",INDEX(SSName,{cl}${CS_R_COL}+1))', P.FONT)
        ws[f'{cl}{CS_R_NAME}'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[CS_R_NAME].height = 54
    lastk = P.L(CS_C0 + SS_SLOTS - 1)
    P.band(ws, CS_KEY_R0 - 1, 'Key results in the chosen year: level, difference and % difference vs the first slot',
           CS_C0 + SS_SLOTS - 1)
    fmt = dict(P.MTO_INDICATORS)
    val = lambda stem_cell, idc, ycol: (f'IFERROR(INDEX(SSAll,MATCH({stem_cell},SSStem,0),MATCH({idc},SSScen,0)'
                                        f'+{ycol}),"")')
    for i, (stem, lab) in enumerate(P.SC_KEY):
        r = CS_KEY_R0 + 3 * i
        for j, (sub, f_) in enumerate([(lab, fmt[stem]), ('  difference vs the first slot', fmt[stem]),
                                       ('  % difference vs the first slot', '0.0%')]):
            rr = r + j
            P.put(ws, f'A{rr}', stem, P.FONT_HELP)
            P.put(ws, f'B{rr}', sub, P.FONT_B if j == 0 else P.FONT)
            P.put(ws, f'C{rr}', f'=IFERROR(INDEX(SSUnit,MATCH($A{rr},SSStem,0)),"")' if j < 2 else '%', P.FONT)
            for k in range(SS_SLOTS):
                cl = P.L(CS_C0 + k)
                if j == 0:
                    f = f'=IF({cl}${CS_R_ID}="","",{val(f"$A{rr}", f"{cl}${CS_R_ID}", "SCYc")})'
                elif j == 1:
                    f = f'=IF(OR({cl}{r}="",${P.L(CS_C0)}{r}=""),"",{cl}{r}-${P.L(CS_C0)}{r})'
                elif stem in P.SC_PCT_KEYS:
                    f = f'=IF(OR({cl}{r}="",N(${P.L(CS_C0)}{r})=0),"",{cl}{r}/${P.L(CS_C0)}{r}-1)'
                else:
                    f = None
                if f:
                    P.put(ws, f'{cl}{rr}', f, P.FONT_B if j == 0 else P.FONT, P.F_BASE if k == 0 else None, f_)
            P.border_bottom(ws, r + 2, 2, CS_C0 + SS_SLOTS - 1)
    P.band(ws, CS_TS_R0 - 1, 'Time series (choose the indicator in the dropdown of each title; chart beside each table)',
           CS_Y1)
    cat = [st for st, _f in P.MTO_INDICATORS if not st.startswith(P.SC_NO_LIST)]
    cr0 = CS_TS_R0 + len(P.SC_TS) * CS_TS_H + 2
    cr1 = cr0 + len(cat) - 1
    P.band(ws, cr0 - 1, 'Indicator list (the time-series dropdowns; code stem, description, unit)', 3)
    for k, stem in enumerate(cat):
        r_ = cr0 + k
        P.put(ws, f'A{r_}', stem, P.FONT_HELP)
        P.put(ws, f'B{r_}', f'=IFERROR(INDEX(SSDesc,MATCH($A{r_},SSStem,0)),$A{r_})', P.FONT)
        P.put(ws, f'C{r_}', f'=IFERROR(INDEX(SSUnit,MATCH($A{r_},SSStem,0)),"")', P.FONT)
    for nm, col in (('CSCatStem', 'A'), ('CSCatLab', 'B'), ('CSCatUnit', 'C')):
        wb.defined_names[nm] = DefinedName(nm, attr_text=f'CompareStored!${col}${cr0}:${col}${cr1}')
    for i, stem in enumerate(P.SC_TS):
        h = CS_TS_R0 + i * CS_TS_H
        yr, s0 = h + 1, h + 2
        P.put(ws, f'B{h}', f'=$B${cr0 + cat.index(stem)}', P.FONT_B, P.F_INPUT)
        dv = DataValidation(type='list', formula1=f'=$B${cr0}:$B${cr1}', allow_blank=False)
        ws.add_data_validation(dv)
        dv.add(f'B{h}')
        P.put(ws, f'A{h}', f'=INDEX(CSCatStem,MATCH($B{h},CSCatLab,0))', P.FONT_HELP)
        P.put(ws, f'C{h}', f'=INDEX(CSCatUnit,MATCH($B{h},CSCatLab,0))', P.FONT_B)
        P.put(ws, f'C{yr}', 'Year', P.FONT_B)
        for k in range(P.NY):
            P.put(ws, f'{P.L(CS_C0 + k)}{yr}', P.BASE_YEAR + k, P.FONT_B, P.F_BASE if k == 0 else None, '0')
        P.border_bottom(ws, yr, 3, CS_Y1)
        for j in range(SS_SLOTS):
            r = s0 + j
            n_ = f'ROWS($B${s0}:B{r})'
            P.put(ws, f'A{r}', f'=$A${h}', P.FONT_HELP)
            P.put(ws, f'B{r}', f'=INDEX(${P.L(CS_C0)}${CS_R_ID}:${lastk}${CS_R_ID},{n_})', P.FONT_HELP, None, '0')
            P.put(ws, f'C{r}', f'=INDEX(${P.L(CS_C0)}${CS_R_SHORT}:${lastk}${CS_R_SHORT},{n_})', P.FONT_B)
            for k in range(P.NY):
                cl = P.L(CS_C0 + k)
                P.put(ws, f'{cl}{r}', f'=IF($B{r}="",NA(),{val(f"$A{r}", f"$B{r}", f"MATCH({cl}${yr},SCYear,0)")})',
                      P.FONT, None, '#,##0.00')
        rng = f'{P.L(CS_C0)}{s0}:{P.L(CS_Y1)}{s0 + SS_SLOTS - 1}'
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'ISNA({P.L(CS_C0)}{s0})'],
                                                       font=P.Font(color='FFFFFF')))
        ch = LineChart()
        ch.title = P.SC_KEY[0][1] if stem == P.SC_KEY[0][0] else stem
        for j in range(SS_SLOTS):
            ser = Series(Reference(ws, min_col=CS_C0, max_col=CS_Y1, min_row=s0 + j, max_row=s0 + j))
            ser.tx = SeriesLabel(strRef=StrRef(f"'CompareStored'!$C${s0 + j}"))
            ser.smooth = False
            ser.marker.symbol = 'none'
            ser.graphicalProperties.line.solidFill = P.SC_COLOURS[j % len(P.SC_COLOURS)]
            ch.series.append(ser)
        ch.set_categories(Reference(ws, min_col=CS_C0, max_col=CS_Y1, min_row=yr, max_row=yr))
        ch.x_axis.delete = ch.y_axis.delete = False
        ch.legend.position = 'b'
        ch.display_blanks = 'gap'
        ch.height, ch.width = 7.5, 16.0
        ws.add_chart(ch, f'{P.L(CS_Y1 + 2)}{h}')
    ws.freeze_panes = f'{P.L(CS_C0)}{CS_R_NAME + 1}'
    for col, wd in {'A': 8, 'B': 44, 'C': 16}.items():
        ws.column_dimensions[col].width = wd
    ws.column_dimensions['A'].hidden = True
    for k in range(P.NY):
        ws.column_dimensions[P.L(CS_C0 + k)].width = 11
    for r in (CS_R_YC, CS_R_COL):
        ws.row_dimensions[r].hidden = True
    wb.defined_names['SCYc'] = DefinedName('SCYc', attr_text=f'CompareStored!$C${CS_R_YC}')
    ws.sheet_view.zoomScale = ZOOM
    ws.sheet_properties.tabColor = '00AE49'


def vba_source():
    text = open(BAS, encoding='cp1252').read()
    assert text.startswith('Attribute VB_Name = "CPATMaster"')
    fm_last = max(P.FM_ROW.values())
    consts = [
        ('MASTER_VERSION', f'"{VERSION}"', 'String'), ('SHIP_LAST', P.SHIP_LAST_YEAR, 'Long'),
        ('LAST_YEAR', P.LAST_YEAR, 'Long'), ('NYEARS', P.NY, 'Long'), ('GW', P.GW, 'Long'),
        ('COL_FILE', COL_FILE, 'Long'), ('COL_URL', COL_URL, 'Long'), ('COL_ACT', COL_ACT, 'Long'),
        ('COL_FILL', COL_FILL, 'Long'), ('COL_LAST', COL_LAST, 'Long'), ('XL_XLSB', 50, 'Long'),
        ('AUTOSEC_FORCE_DISABLE', 3, 'Long'), ('DATA_FILE', '"CPAT_LegacyData.xlsx"', 'String'),
        ('DL_MAXROWS', 60000, 'Long'), ('SH_MT', '"ScenarioDefinition"', 'String'), ('SH_MIT', '"Mitigation"', 'String'),
        ('SH_OUT', '"MTOutputs"', 'String'), ('SH_SS', '"StoredScenarios"', 'String'),
        ('SH_FM', '"FromMitigation"', 'String'), ('EXPORT_NAME', '"ExportDistn"', 'String'),
        ('FM_FIRST', P.FM_R0, 'Long'), ('FM_LAST', fm_last, 'Long'), ('FM_COL_FIRST', P.COL_G0, 'Long'),
        ('FM_COL_LAST', P.CI_('IZ'), 'Long'),
        ('OUT_COL_G0', P.COL_G0, 'Long'), ('OUT_ROW_SCEN', 5, 'Long'), ('OUT_ROW_NAME', 4, 'Long'),
        ('SS_COL_G0', P.COL_G0, 'Long'), ('SS_SLOTS', SS_SLOTS, 'Long'), ('SS_FIRST', P.MTO_R0, 'Long'),
        ('SS_LAST', P.MTO_LAST, 'Long'), ('SS_ROW_ID', SS_ROW_ID, 'Long'), ('SS_ROW_NAME', SS_ROW_NAME, 'Long'),
        ('SS_ROW_META', SS_ROW_META, 'Long'),
        ('MT_ROW_RUN', 4, 'Long'), ('MT_ROW_NUM', P.MT_ROW_SCEN, 'Long'), ('MT_ROW_NAME', P.MT_ROW_NAME, 'Long'),
        ('MT_FIRST', 8, 'Long'), ('MT_LAST', P.MT_END, 'Long'), ('MT_ROW_ID', 10, 'Long'), ('MT_ROW_IDNAME', 12, 'Long'),
        ('MT_COL_PARAM', 8, 'Long'), ('MT_COL_FIRST', P.MT_COL0, 'Long'), ('MIT_ROW_SCEN', P.R_SCEN, 'Long'),
        ('MIT_COL_FIRST', P.COL_G0, 'Long'), ('MIT_MAX_ROW', P.MIT_MAX, 'Long'), ('LIVE_SCEN', 2, 'Long'),
        ('BASE_SCEN', 1, 'Long'), ('ETS_TOL', 0.005, 'Double'), ('ETS_MAXITER', 20, 'Long')]
    block = '\n'.join(f'Private Const {n} As {t} = {v}' for n, v, t in consts)
    assert "' @@CONSTANTS@@" in text
    return text.split('\n', 1)[1].replace("' @@CONSTANTS@@", "' constants written by build_master.py\n" + block)


def compile_test(path):
    """The VBA project compiles: LibreOffice (VBA mode) runs MasterVersion, which returns None when the module does
    not compile (NORMS 3j: a module variable M shadowed by a local m, case-insensitive, made M.Queries invalid)."""
    import subprocess
    import sys
    out = subprocess.run([sys.executable, os.path.join(P.HERE, 'checks', 'lo_run_macro.py'), path,
                          'CPATMaster.MasterVersion', os.path.join(tempfile.mkdtemp(), 'compile.xlsx')],
                         capture_output=True, text=True, timeout=600).stdout
    assert f"returned '{VERSION}'" in out, f'the VBA module does not compile (LibreOffice): {out[-300:]}'
    print('VBA compiles (LibreOffice VBA mode): MasterVersion =', VERSION)


def main():
    wb = Workbook()
    build_guide(wb)
    build_settings(wb)
    ids = build_stored(wb)
    build_compare(wb)
    wb.active = 0
    for w in wb.worksheets:
        w.sheet_view.tabSelected = w.title == 'UserGuide'
        w.sheet_format.defaultColWidth = P.COL_W
    wb.code_name = 'ThisWorkbook'
    for k, w in enumerate(wb.worksheets, 1):
        w.sheet_properties.codeName = f'Sheet{k}'
    from vba_project import embed_vba
    tmp = os.path.join(tempfile.mkdtemp(), f'{NAME}.xlsx')
    wb.save(tmp)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    embed_vba(tmp, OUT, {'CPATMaster': vba_source()})
    P.add_macro_buttons(OUT, 'UserGuide', BUTTONS, col0=BTN_COL0, row0=BTN_ROW0, colour='00B050', across=1)
    P.store_values(OUT)                             # the values of the comparison (LibreOffice)
    import excel_lint
    problems = excel_lint.lint(OUT)
    if problems:
        raise SystemExit(f'{OUT}: Excel would repair it:\n  ' + '\n  '.join(problems))
    compile_test(OUT)
    P.REL.publish(OUT)
    os.makedirs(os.path.dirname(ACTIVE_COPY), exist_ok=True)
    shutil.copy(OUT, ACTIVE_COPY)
    print(f'saved {OUT} and {ACTIVE_COPY}; stored slots: scenario IDs {ids}')


if __name__ == '__main__':
    main()
