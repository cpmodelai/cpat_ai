"""CPAT-AI Distribution Prototype: the standalone distribution module (Plan_Modules M3).

The module is cut from the built mitigation prototype (one source of truth: the prototype builder's Distribution,
FromMitigation and data tabs, not a second copy of them). From ../permalink/CPAT-AI-Mitigation-Prototype_latest.xlsm it keeps
the tabs the Distribution tab reads, turns every formula that reads a dropped tab into its value (FromMitigation
entirely: the button Update from Mitigation refreshes it), keeps the defined names and LAMBDAs still used, shows only
the distribution rows of ScenarioDefinition, and adds a Cover with the link to the mitigation workbook and the VBA
module CPATDistribution.bas. Then, as the prototype: shipped with its values (LibreOffice), manual calculation,
linted.

    python build_distribution.py       # writes ../CPAT-AI-Distribution-Prototype_v<version>.xlsm (older versions to
                                       # ../releases/; NORMS 5a; about 2 min)
"""
import os
import re
import shutil
import sys
import tempfile
import time

import openpyxl
from openpyxl.styles import Alignment, Border
from openpyxl.workbook.defined_name import DefinedName

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mitigation'))
sys.path.insert(0, os.path.join(HERE, '..', 'shared'))
import build as P                                      # noqa: E402  the prototype builder (helpers, layout)

VERSION = '1.0.0'
NAME = 'CPAT-AI-Distribution-Prototype'
OUT = P.REL.versioned(NAME, VERSION, 'xlsm')     # v0.1.1: excel_ai/<name>_v<version>.xlsm (_latest copies: NORMS 5a)
SOURCE = P.LATEST                                     # the mitigation prototype the module is cut from
BAS = os.path.join(HERE, 'CPATDistribution.bas')
MIT_FILE = os.path.basename(P.LATEST)

VERSION_LOG = [  # version, date, change
    ('0.1.0', '2026-10-22', f'First standalone module, cut from the mitigation prototype v{P.VERSION}: its Distribution '
                          'and FromMitigation tabs, the distribution data tabs, the distribution rows of '
                          'ScenarioDefinition and Settings. Inputs from Mitigation by the button Update from '
                          'Mitigation (section 19a, defined name ExportDistn).'),
    ('0.1.1', '2026-10-28', f'Cut from the mitigation prototype v{P.VERSION}: ScenarioDefinition on the rows of legacy '
                          '465 with a complete set of names (bug L137, issue I87); the mitigation workbook is looked '
                          'for in permalink/ too; file named _v0.1.1 at the top of excel_ai/ (NORMS 5a).'),
    ('0.1.2', '2026-10-29', f'Cut from the mitigation prototype v{P.VERSION} (combustion emission factors as legacy, '
                          'issue I98; data problems as issues).'),
    ('0.1.3', '2026-10-29', f'Cut from the mitigation prototype v{P.VERSION} (remaining functionality, reverts to legacy, '
                          'data from legacy 465, last historical price year 2024); the Distribution method unchanged.'),
    ('0.1.4', '2026-10-29', f'Cut from the mitigation prototype v{P.VERSION}: bug M22 fixed (found by Coded CPAT): the '
                          '25th/75th percentile recycling rows (hrec) add the public investment amount per person '
                          '(pui of the sample, LCU), not its % row.'),
    ('1.0.0', '2026-10-29', f'First full release (user 2026-10-29), cut from the mitigation prototype v{P.VERSION}: '
                          'Distribution 0.1.4 as released. Replicated number for number by Coded CPAT 1.0.0p1.0.'),
]

# the tabs of the module, in order (Cover is added); everything else of the prototype is dropped
TABS = ['ScenarioDefinition', 'FromMitigation', 'Distribution', 'Settings', 'DATA_DISTN->>', 'DistMapping',
        'IO_GTAP', 'HHSurvey', 'HH_Elast', 'ASPIRE', 'WHOCooking', 'GDPRatios', 'WEO']
TAB_INFO = [  # tab, content
    ('Cover', 'This page: what the module is, the link to the mitigation workbook, the buttons'),
    ('ScenarioDefinition', 'The distribution settings of each scenario (the other rows, set in the mitigation '
                           'workbook, are hidden)'),
    ('FromMitigation', 'The inputs from Mitigation (section 19a of the mitigation workbook): values, refreshed by '
                       'Update from Mitigation'),
    ('Distribution', 'The model: household incidence by decile in the analysis year, one column group per scenario'),
    ('Settings', 'Constants and lookups (the mitigation ones are values here)'),
    ('DistMapping ... WEO', 'The data tabs: mappings, input-output table, household survey, elasticities, ASPIRE, '
                            'cooking fuels, GDP ratios, WEO'),
]
MACRO_BUTTONS = [('Update from Mitigation', 'UpdateFromMitigation'), ('Recalculate now', 'RecalculateNow'),
                 ('Recalculation on/off', 'ToggleRecalculation')]

SHEET_REF = re.compile(r"'((?:[^']|'')+)'!|([A-Za-z_][\w.]*(?:->>)?)!")
TOKEN = re.compile(r'(?<![\w.])([A-Za-z_][\w.]*)')


def sheets_in(text):
    return {(m.group(1) or '').replace("''", "'") or m.group(2) for m in SHEET_REF.finditer(text)}


def tokens(text):
    return set(TOKEN.findall(re.sub(r'"[^"]*"', '""', text)))


def export_values(wbv):
    """{FromMitigation row: values of columns K..IZ} of the prototype's section 19a (defined name ExportDistn), mapped
    as the macro UpdateFromMitigation maps them: years to row 1, scenario numbers to row 5, the data rows from FM_R0."""
    m = re.match(r"(\w+)!\$A\$(\d+):\$([A-Z]+)\$(\d+)", wbv.defined_names['ExportDistn'].attr_text)
    ws, r0, r1 = wbv[m.group(1)], int(m.group(2)), int(m.group(4))
    rows = [1, 5] + list(range(P.FM_R0, P.FM_R0 + r1 - r0 - 1))
    return {fr: [ws.cell(r0 + i, c).value for c in range(P.COL_G0, P.CI_('IZ') + 1)] for i, fr in enumerate(rows)}


def cut(wb, wbv, log=print):
    """Drop the prototype's other tabs; formulas that read them become values; unused names go."""
    keep = set(TABS)
    for t in [t for t in wb.sheetnames if t not in keep]:
        del wb[t]
    names = {n: d.attr_text for n, d in wb.defined_names.items()}
    bad = {n for n, v in names.items() if sheets_in(v) - keep}
    while True:                                        # names that read a bad name are bad too
        more = {n for n, v in names.items() if n not in bad and tokens(v) & bad}
        if not more:
            break
        bad |= more
    used = set()
    n_val = {}
    for ws in wb.worksheets:
        wv = wbv[ws.title]
        k = 0
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not (isinstance(v, str) and v.startswith('=')):
                    continue
                if ws.title == 'FromMitigation' or sheets_in(v) - keep or tokens(v) & bad:
                    c.value = wv.cell(c.row, c.column).value
                    k += 1
                else:
                    used |= tokens(v) & set(names)
        n_val[ws.title] = k
        for link in list(ws._hyperlinks):
            if link.location and sheets_in(link.location + '!') - keep:
                ws._hyperlinks.remove(link)
    while True:                                        # names read by the names in use (LAMBDA bodies)
        more = {t for n in used for t in tokens(names[n]) & set(names)} - used
        if not more:
            break
        used |= more
    assert not used & bad, used & bad
    for n in [n for n in names if n not in used]:
        del wb.defined_names[n]
    fm, ex = wb['FromMitigation'], export_values(wbv)
    for r, vals in ex.items():                         # as Update from Mitigation writes them (blank stays blank)
        for c, v in enumerate(vals, P.COL_G0):
            fm.cell(r, c).value = v
    log(f'  formulas turned into values: {n_val}')
    log(f'  defined names kept: {len(used)} of {len(names)} ({len(bad)} read dropped tabs)')
    return n_val


def show_distribution_rows(ws, wsd, wsdv):
    """ScenarioDefinition: rows 1-8 (headings, scenario numbers and names, country) and the rows Distribution reads
    (its column D: the ScenarioDefinition row of each setting), each under its heading row; the rest hidden."""
    rows = {wsdv.cell(r, 4).value for r in range(1, wsd.max_row + 1)
            if isinstance(wsd.cell(r, 4).value, str) and 'MTRowNum' in wsd.cell(r, 4).value}
    assert rows and all(isinstance(r, (int, float)) and r == int(r) for r in rows), rows
    rows = {int(r) for r in rows}
    show = set(range(1, 9)) | rows
    for r in rows:
        h = r
        while h > 8 and not (ws.cell(h, 2).value and not ws.cell(h, 8).value):
            h -= 1
        show.add(h)
    for r in range(9, ws.max_row + 1):
        ws.row_dimensions[r].hidden = r not in show
    P.put(ws, 'J1', 'Distribution module: only the distribution rows are shown (the other rows are set in the '
                    'mitigation workbook). Scenario numbers (row 5) as in the mitigation workbook.', P.FONT_B)
    return sorted(rows)


def build_cover(wb):
    ws = wb.create_sheet('Cover', 0)
    w = 4
    P.bar(ws, 2, f'{NAME} v{VERSION}: Cover page', w, P.F_TITLE, P.FONT_T)
    P.put(ws, 'A3', 'The distribution module of the Climate Policy Assessment Tool (CPAT): the effect of the '
                    'scenarios of the mitigation prototype on households, by decile, in one analysis year.')
    r = 5
    P.bar(ws, r, 'How to use it (one scenario at a time)', w, P.F_BAND, P.FONT_SUBBAR)
    steps = ['In the mitigation workbook: define the scenario, Recalculate now, save (or leave it open).',
             'Here: click Update from Mitigation. It copies section 19a of the mitigation workbook into '
             'FromMitigation and recalculates.',
             'Read the results on Distribution (one column group per scenario, deciles across).',
             'Distribution settings of a scenario (analysis year, revenue recycling, targeting): ScenarioDefinition, '
             'then Recalculate now.']
    for k, s in enumerate(steps, 1):
        P.put(ws, f'A{r + k}', f'{k}.', P.FONT_B)
        P.put(ws, f'B{r + k}', s)
    r += len(steps) + 2
    P.bar(ws, r, 'Link to the mitigation workbook', w, P.F_BAND, P.FONT_SUBBAR)
    lines = [('Mitigation workbook (input)', MIT_FILE, 'MitSource', P.F_INPUT),
             ('', 'A name alone is looked for next to this workbook, then one folder up; or a full path or web '
                  'address', None, None),
             ('File used by the last update', 'none (shipped values)', 'MitUsed', None),
             ('Last update', f'shipped: values of {MIT_FILE} v{P.VERSION}', 'MitLastUpdate', None),
             ('Country (Settings C4)', '=CtryCode', None, None),
             ('Calculation', 'Shipped with its values, manual calculation: Recalculate now, or Recalculation on/off',
              None, None)]
    for k, (lab, v, nm, f_) in enumerate(lines, r + 1):
        P.put(ws, f'A{k}', lab, P.FONT_B)
        P.put(ws, f'B{k}', v, P.FONT, f_)
        if nm:
            wb.defined_names[nm] = DefinedName(nm, attr_text=f'Cover!$B${k}')
    r += len(lines) + 2
    P.bar(ws, r, 'Contents', w, P.F_BAND, P.FONT_SUBBAR)
    for j, h in enumerate(['Tab', 'Content'], 1):
        P.put(ws, f'{P.L(j)}{r + 1}', h, P.FONT_B).border = Border(bottom=P.THIN)
    for k, (t, s) in enumerate(TAB_INFO, r + 2):
        P.put(ws, f'A{k}', t)
        P.put(ws, f'B{k}', s)
    r += len(TAB_INFO) + 3
    P.bar(ws, r, 'Limits', w, P.F_BAND, P.FONT_SUBBAR)
    for k, s in enumerate([f'The data tabs and the Settings lookups are those of the prototype v{P.VERSION} '
                           '(Egypt). Another country needs its own data tabs; its Mitigation inputs come from the '
                           'mitigation workbook of that country.',
                           'The scenario columns of ScenarioDefinition must carry the scenario numbers of the '
                           'mitigation workbook (FromMitigation row 5).'], r + 1):
        P.put(ws, f'B{k}', s)
    r += 4
    P.bar(ws, r, 'Version log', w, P.F_BAND, P.FONT_SUBBAR)
    for j, h in enumerate(['Version', 'Change', 'Date'], 1):
        P.put(ws, f'{P.L(j)}{r + 1}', h, P.FONT_B).border = Border(bottom=P.THIN)
    for k, (v, d, s) in enumerate(VERSION_LOG, r + 2):
        P.put(ws, f'A{k}', v)
        P.put(ws, f'B{k}', s).alignment = Alignment(wrap_text=True, vertical='top')
        P.put(ws, f'C{k}', d).alignment = Alignment(vertical='top')
    for col, wd in {'A': 30, 'B': 120, 'C': 12, 'D': 12}.items():
        ws.column_dimensions[col].width = wd
    ws.sheet_properties.tabColor = P.F_TABDIV
    return ws


def vba_source():
    text = open(BAS, encoding='cp1252').read()
    assert text.startswith('Attribute VB_Name = "CPATDistribution"')
    for const, want in (('FM_FIRST', P.FM_R0), ('FM_LAST', max(P.FM_ROW.values())),
                        ('FM_COL_FIRST', P.COL_G0), ('FM_COL_LAST', P.CI_('IZ'))):
        m = re.search(rf'Private Const {const} As Long = (\d+)', text)
        assert m and int(m.group(1)) == want, f'CPATDistribution {const} {m and m.group(1)} differs from {want}'
    m = re.search(r'Private Const MIT_FILE As String = "([^"]*)"', text)
    assert m and m.group(1) == MIT_FILE, (m and m.group(1), MIT_FILE)
    return text.split('\n', 1)[1]


def main():
    t0 = time.time()
    stage = lambda what: print(f'[{time.time() - t0:5.0f} s] {what}', flush=True)
    wb = openpyxl.load_workbook(SOURCE)
    wbv = openpyxl.load_workbook(SOURCE, data_only=True)
    stage(f'loaded {os.path.basename(SOURCE)}')
    sd_rows = show_distribution_rows(wb['ScenarioDefinition'], wb['Distribution'], wbv['Distribution'])
    print(f'  ScenarioDefinition rows read by Distribution: {len(sd_rows)} ({sd_rows[0]}-{sd_rows[-1]})')
    cut(wb, wbv)
    build_cover(wb)
    wb._sheets = [wb[n] for n in ['Cover'] + TABS]
    wb.active = 0
    for w in wb.worksheets:
        w.sheet_view.tabSelected = w.title == 'Cover'
    wb.calculation.fullCalcOnLoad = False
    wb.code_name = 'ThisWorkbook'
    for k, w in enumerate(wb.worksheets, 1):
        w.sheet_properties.codeName = f'Sheet{k}'
    from vba_project import embed_vba
    tmp = os.path.join(tempfile.mkdtemp(), f'{NAME}-v{VERSION}.xlsx')
    wb.save(tmp)
    P.fix_outline_levels(tmp)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    embed_vba(tmp, OUT, {'CPATDistribution': vba_source()})
    P.add_macro_buttons(OUT, 'Cover', MACRO_BUTTONS, col0=2, row0=5, across=3)
    stage('saved, macros and buttons added')
    P.store_values(OUT)
    import excel_lint
    problems = excel_lint.lint(OUT)
    if problems:
        raise SystemExit(f'{OUT}: Excel would repair it:\n  ' + '\n  '.join(problems))
    P.REL.publish(OUT, link=True)                      # v0.1.1: older versions to releases/; _latest in both permalink folders
    stage(f'calculated values stored, linted; saved {OUT}')


if __name__ == '__main__':
    main()
