"""Legacy_CPAT_Bugs_v<version>.docx (excel_ai/bugs_and_legacy/): the legacy CPAT bugs, kept like a stock book (v0.8.4, user 2026-10-28).

Front: the rule (bugs and issues; data problems are issues), then one table of every legacy bug found, fixed in the
prototype and fixed (or not) in legacy 465, then the data problems with their priority. Then each bug in detail by type (engineer power,
engineer road transport, other mitigation by area, distribution, inputs), with its cell-level fix plan; the bugs the
CPAT team fixed in 465 in appendices. Issues (data included), prototype bugs, departures, upgrades and the bug-fixing
procedure are in the Documentation (appendices) and the tracker Tracking_Legacy_Bugs_v<version>.xlsx; every code
cross-refers.

Sources: register.py (one record per item: issues_register.py, make_legacy_fixes.py, build.py LegacyDiff, the cell
plans in excel_ai/bugs_and_legacy/fixes/data, the 465 check in excel_ai/bugs_and_legacy/fixes/check465).

    python make_bugfix_book.py        (needs python-docx)
"""
import os as _os, sys as _sys  # the excel_ai code folders and data/scripts on the path (core/tools/xlpaths.py)
_xl = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_xl) != 'excel_ai':
    _xl = _os.path.dirname(_xl)
_sys.path.insert(0, _os.path.join(_xl, 'core', 'tools'))
import xlpaths  # noqa: E402,F401
import datetime
import functools
import json
import os
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import build as B
import issues_register as R
import make_legacy_fixes as M
import power_model_ref as PM
import register as G

HERE = xlpaths.MIT                     # excel_ai/mitigation/ (the script sits in a subfolder)
ROOT = os.path.dirname(HERE)                 # excel_ai/ (restructure 2026-10-22)
PLANS = os.path.join(ROOT, 'bugs_and_legacy', 'fixes', 'data')   # v0.7.1: was excel_ai/bugs_and_legacy/fixes/
DOC_NAME = 'Legacy_CPAT_Bugs'
OUT = B.REL.versioned(DOC_NAME, R.REGISTER_VERSION, 'docx')   # v0.8.4: excel_ai/bugs_and_legacy/Legacy_CPAT_Bugs_v<version>.docx
TRACKER_NAME = 'Tracking_Legacy_Bugs'
HEAD, LIGHT, PALE = 'D9E8C4', 'F2F2F2', 'EBF1DE'
RED = RGBColor(0xC0, 0x00, 0x00)
LEGACY_FILE = 'CPAT 1.0pre_465_NoPropData.xlsb'   # v0.8.4: the copy in legacy/workbooks (bugsfixed/ retired)
CHECK465 = os.path.join(ROOT, 'bugs_and_legacy', 'fixes', 'check465', 'legacy465_check.json')   # the fixes the CPAT team made in 465, checked 2026-10-22
MARK = {'Confirmed fixed': 'CONFIRMED in 465', 'Fixed with caveats': 'FIXED WITH CAVEATS in 465',
        'Not fixed': 'NOT FIXED in 465'}
POWER = ({f'L{k}' for k in range(1, 13)} | {f'L{k}' for k in range(52, 57)}
         | {'L67', 'L83', 'L84', 'L88', 'L95'}
         | {f'L{k}' for k in range(107, 112)} | {'L126', 'L127'})   # v0.5.4: power features; v0.7.1: L126, L127   # engineer power model (L83, L84: electricity subsidies; L88: power)
TRANSPORT = {f'L{k}' for k in range(25, 42)}                                          # engineer road model
TYPE_NAME = {'power': 'Engineer power', 'transport': 'Engineer transport', 'other': 'Other mitigation',
             'dist': 'Distribution', 'inputs': 'Inputs (ScenarioDefinition)'}


# ---------------------------------------------------------------- the data
def bug_type(code):
    return 'power' if code in POWER else 'transport' if code in TRANSPORT else 'other'


def plans():
    """Cell-level plans by bug id: every plan file of excel_ai/bugs_and_legacy/fixes/data (one loader, register.py; until
    2026-10-29 this kept its own list and missed fixes_v0_9_0.json, so L171-L229 printed "not written yet")."""
    return G.plans()


def other_sections():
    """v0.7.1: other-mitigation bugs by model area (excel_ai/bugs_and_legacy/fixes/data/cfg_other_sections.json), sections in
    rough priority order; a bug the file does not list goes to a last section."""
    cfg = json.load(open(os.path.join(PLANS, 'cfg_other_sections.json'), encoding='utf-8'))
    return [(s['title'], s['intro'], s['ids']) for s in cfg['sections']]


def _btype(r):
    return {'Distribution': 'dist', 'Inputs (ScenarioDefinition)': 'inputs',
            'Mitigation: engineer power': 'power', 'Mitigation: engineer road transport': 'transport'}.get(r['area'],
                                                                                                       'other')


def legacy_bugs():
    """Every legacy bug of the mitigation sheets and the inputs: (code, type, title, where, what legacy does, fix,
    prototype status, priority, effect), from the register."""
    return [(r['id'], _btype(r), r['title'], r['where'], r['description'], r['fix'], r['prototype'], r['priority'],
             r['effect']) for r in G.by_kind('L') if _btype(r) != 'dist']


def dist_bugs():
    return [(r['id'], 'dist', r['title'], r['where'], r['description'], r['fix'], r['prototype'], r['priority'],
             r['effect']) for r in G.by_kind('L') if _btype(r) == 'dist']


@functools.lru_cache(maxsize=None)
def check465():
    """{code: {status, note}} of the bugs the CPAT team marked fixed in legacy 465 (v0.8.2)."""
    return json.load(open(CHECK465, encoding='utf-8'))['bugs'] if os.path.exists(CHECK465) else {}


def legacy_status(code):
    """(status in legacy 465, note) of a legacy bug."""
    c = check465().get(code)
    if c is None:
        return 'Open in legacy 465 (not marked fixed by the CPAT team)', ''
    return {'Confirmed fixed': 'Fixed in legacy 465 (confirmed)',
            'Fixed with caveats': 'Fixed with caveats in legacy 465',
            'Not fixed': 'Marked fixed by the CPAT team, but not fixed in legacy 465'}[c['status']], c['note']


def moved(code):
    """'B' (fixed with caveats or not fixed in 465) or 'C' (fixed, confirmed) for a bug that goes to an appendix."""
    c = check465().get(code)
    return None if c is None or code.startswith('I') else ('C' if c['status'] == 'Confirmed fixed' else 'B')


# ---------------------------------------------------------------- Word helpers
def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement('w:tblHeader')
    el.set(qn('w:val'), 'true')
    trPr.append(el)


TEXT_W = 17.0                           # cm between the margins (A4, 2 cm margins)
BREAK = re.compile(r'([,;:(+\-*/=<>&!])')   # v0.5.4: break opportunities in long formulas (zero-width space after)


def fit_widths(t, widths):
    """v0.5.4 (user: tables overflowed on the right, left columns too wide): fixed layout, the grid and every cell
    set to the column widths (Word lays out by the grid), scaled down to the text width when wider."""
    k = min(1.0, TEXT_W / sum(widths))
    w = [Cm(x * k) for x in widths]
    tblPr = t._tbl.tblPr
    for tag, attrs in (('w:tblW', {'w:w': str(int(sum(x * k for x in widths) / 2.54 * 1440)), 'w:type': 'dxa'}),
                       ('w:tblLayout', {'w:type': 'fixed'})):
        el = tblPr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            tblPr.append(el)
        for a, v in attrs.items():
            el.set(qn(a), v)
    for gc, x in zip(t._tbl.tblGrid.findall(qn('w:gridCol')), w):
        gc.set(qn('w:w'), str(int(x.twips if hasattr(x, 'twips') else x / 635)))
    for row in t.rows:
        for c, x in zip(row.cells, w):
            c.width = x


def text(cell, s, size=8.5, bold=False, mono=False):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    if mono and s:
        s = BREAK.sub('\\1\u200b', s)
    r = p.add_run(s or '')
    r.font.size = Pt(size)
    r.bold = bold
    r.font.name = 'Consolas' if mono else 'Arial'
    return p


def table(doc, header, rows, widths, size=8.5, mono_cols=()):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.width = Cm(widths[i])
        shade(c, HEAD)
        text(c, h, size, bold=True)
    repeat_header(t.rows[0])
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            text(cells[i], '' if v is None else str(v), size, mono=i in mono_cols)
    fit_widths(t, widths)
    doc.add_paragraph()
    return t


def para(doc, s, bold_lead=None, size=10, style=None):
    p = doc.add_paragraph(style=style)
    if bold_lead:
        r = p.add_run(bold_lead + ' ')
        r.bold = True
        r.font.size = Pt(size)
    r = p.add_run(s)
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(4)
    return p


def bullets(doc, items, size=10):
    for s in items:
        p = doc.add_paragraph(style='List Bullet')
        r = p.add_run(s)
        r.font.size = Pt(size)


def toc(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    for kind, txt in (('begin', None), (None, 'TOC \\o "1-2" \\h \\z \\u'), ('separate', None), (None, None),
                      ('end', None)):
        if kind:
            el = OxmlElement('w:fldChar')
            el.set(qn('w:fldCharType'), kind)
            run._r.append(el)
        elif txt:
            el = OxmlElement('w:instrText')
            el.set(qn('xml:space'), 'preserve')
            el.text = txt
            run._r.append(el)
        else:
            t = OxmlElement('w:t')
            t.text = 'Right-click and choose Update Field to show the table of contents.'
            run._r.append(t)


# ---------------------------------------------------------------- the document
def procedure_steps(doc):
    doc.add_heading('2. The bug-fixing procedure', 1)
    doc.add_heading('2.1 The two protocols of the legacy workbook', 2)
    para(doc, 'Legacy CPAT relies on two conventions that a fix must keep, and that many bugs break:')
    table(doc, ['Protocol', 'What it means', 'Test'], [
        ('Drag left to right', 'Every year cell of a row holds the same formula in relative (R1C1) form, so a '
         'row can be dragged from its first year to the last.', 'One R1C1 formula per row from the first '
         'projected year to the last.'),
        ('Copy-paste baseline to policy', 'The policy block repeats the baseline block a fixed number of rows '
         'down: in legacy 465, +6,316 rows throughout, from row 2173 (names BaselineFirstRow, PolicyScenarioFirstRow; '
         'policy row 8489) to the end of the results sub-blocks (row 8403 maps to 14719). In 456 it was +6,331 to '
         'about row 6070 and +6,317 after it.', 'The policy row equals '
         'the baseline row in R1C1 form.')], [3.5, 8.0, 4.5])
    doc.add_heading('2.2 Before you start', 2)
    bullets(doc, [
        'Work on a copy of the workbook; never fix the only copy, and save each fixed file as a new version.',
        'Find the cells by label and code (column D labels, column B/C codes), never by a typed row number: rows move '
        'between legacy versions.',
        'Check the register entry still matches the file: the cell must hold the formula the register describes. If '
        'it does not, stop and report (the bug may already be fixed, as many are in the 465 file).',
        'Fix in order of priority (High first): High changes the results of the standard Egypt runs; Medium changes '
        'some runs, countries or reported numbers; Low is latent or cosmetic.',
        'A fix in the baseline block is pasted into the policy block (section 2.1); rows above 2173 are shared and '
        'have no policy copy.'])
    doc.add_heading('2.3 Stages of a fix', 2)
    para(doc, 'The macro bugfix_procedure/FixL1_ServicesElectricity.bas runs these stages for bug L1; the same stages '
              'apply to every bug, by macro or by hand.')
    table(doc, ['Stage', 'Step', 'Pass rule'], [
        ('P Preflight', 'Locate the rows by label and code; find the year columns from row 1; check the block offset '
         '(PolicyScenarioFirstRow - BaselineFirstRow); check the row holds exactly the bug formula in every year of '
         'both blocks.', 'Every item passes; if the formulas are already fixed or differ from the register, stop '
         'before changing anything.'),
        ('S Snapshot', 'Full recalculation, then keep every formula (R1C1) and value of the sheet.', ''),
        ('F Fix', 'Baseline: write the new formula in the first wrong year and fill right (a real drag). Policy: '
         'copy the baseline cells and paste formulas (a real copy-paste). Recalculate fully.', ''),
        ('T1 Drag', 'The row has one R1C1 formula from the first projected year to the last, in both blocks.',
         '0 cells differ'),
        ('T2 Copy-paste', 'Policy row R1C1 = baseline row R1C1.', '0 cells differ'),
        ('T3 Nothing else moved', 'Whole sheet, formulas before against after: exactly the intended cells changed.',
         'intended cells only'),
        ('T4 Independent calculation', 'Recompute the fixed row from the recalculated values outside Excel (VBA or '
         'Python) and compare.', '0 years differ'),
        ('T5 Past unchanged', 'Years before the first fixed year unchanged everywhere (columns that are lags, not '
         'years, are reported, not failed).', '0 changed, else review'),
        ('T6 No new errors', 'The count of error cells does not increase.', 'after <= before'),
        ('T7 Reconciliation', 'The change of the total that the row feeds equals the change of the row (within 5%; '
         'the rest is price feedback).', 'review if > 5%'),
        ('R Report', 'Number of changed rows; the rows with the largest change as a share of their size.',
         'judgement')], [3.0, 9.0, 4.0])
    doc.add_heading('2.4 Applying a cell-level plan', 2)
    para(doc, 'For every bug (the "Cell plan" column says which) the repository holds a cell-level plan '
              '(excel_ai/bugs_and_legacy/fixes/data, JSON): for each cell the formula now, the new formula, the range to fill and the policy row. Apply a '
              'plan as stage F above: type the new formula in the cell, fill the range, copy the baseline cells onto '
              'the policy row given (Paste Special, Formulas), recalculate, then run T1-T7. The plans are printed with '
              'each bug in section 3.')
    para(doc, 'For bugs without a cell plan yet the bug entry gives the legacy rows, what legacy does '
              'and the fix it needs. Write the plan as the existing ones were made (excel_ai/bugs_and_legacy/fixes/tools: build '
              'the new formula by exact text substitution of the legacy formula, stop if the legacy text is not found, '
              'check the brackets), add it to the JSON and regenerate this document.')
    doc.add_heading('2.5 Worked example: bug L1', 2)
    para(doc, 'L1 (services electricity demand grows with the industrial multiple after 2023) breaks both protocols, '
              'so one fix exercises every test: row 3731 holds =RC[-1]*R[-18]C in 2023 and =RC[-1]*R[-24]C from 2024 '
              '(the row cannot be dragged), and policy row 10062 has the same wrong formula (456 rows: the run below '
              'was on the 456 file; in 465 L1 is fixed and the rows are 3713/10029, 3707/10023, 3731/10047, offset '
              '6,316).')
    table(doc, ['Check', 'Result (scratch copy of the 456 NoPropData file, Excel 365, 2026-10-15)'], [
        ('Preflight P1-P6', 'PASS: rows 3713/10044, 3707/10038, 3731/10062; offset 6,331; bug formula in all 18 years '
         'of both blocks'),
        ('Run on a fixed file', 'stops at P5/P6 with FAIL "state = FIXED", nothing changed'),
        ('T1, T2', 'PASS (=RC[-1]*R[-18]C in M:AE, both blocks)'),
        ('T3', 'PASS: 36 of 36 formula cells changed, 0 others'),
        ('T4, T6', 'PASS (2,160 error cells before and after, inherited from the stripped file)'),
        ('T7', 'PASS: other sectors add at most 2.4% (baseline) and 4.1% (policy) of the services change'),
        ('T5', 'REVIEW: 72 cells in column M of the fiscal-multiplier tables, whose columns are lags, not years'),
        ('Effect', '2041 services electricity demand: baseline 6,685 to 8,743 ktoe (+30.8%), policy 5,508 to 6,397 '
         '(+16.1%); 3,979 rows change')], [3.5, 12.5])
    doc.add_heading('2.6 Reusing the harness for the next bug', 2)
    table(doc, ['Part of the macro', 'What to change'], [
        ('Constants (labels, codes, first year)', 'Labels and codes that locate the rows; first year of the wrong '
         'formula'),
        ('Locate', 'How the row is found (by label and code, never a typed row number)'),
        ('RowState', 'The wrong and the right R1C1 formula (the "has CPAT changed" test)'),
        ('ApplyFix', 'The new formula; keep "drag in the baseline, paste into the policy"'),
        ('TestIndependent, TestTotals', 'The independent recomputation and reconciliation of the new bug')],
        [5.0, 11.0])
    para(doc, 'Keep the whole-sheet formula diff (T3), the past-unchanged test (T5), the error count (T6), the FixLog '
              'sheet and "never saves".')
    doc.add_heading('2.7 After the fix', 2)
    bullets(doc, [
        'Record it: the register entry gets "fixed in legacy version x", and the workbook\'s version log a row.',
        'Compare with the prototype: the prototype already computes the fixed behaviour, so a fixed legacy file should '
        'move toward it. The prototype\'s LegacyDiff sheet lists every remaining departure.',
        'Run a policy scenario as well as the baseline (switch MTInputs D6, _ScenarioToRun): T1-T4 must still pass.'])
    doc.add_heading('2.8 Limits', 2)
    bullets(doc, [
        'Tested on the NoPropData file only; the preflight is there to detect a different file and stops without '
        'changing anything.',
        'The macro checks sheet Mitigation only; effects on other sheets (Dashboard, Transport, Distribution) are '
        'not compared.',
        'The report ranks changed rows; it cannot say whether a change is right. The independent check covers the '
        'fixed row; everything downstream is judged by reading the report.',
        'Needs macros enabled and the file kept as .xlsb or .xlsm.'])


def bug_block(doc, b, plan, level=3):
    code, typ, title, where, what, fix, status, pri, effect = b
    h = doc.add_heading(f'{code}  {title}', level)
    c465 = check465().get(code)
    if c465:                                         # v0.8.2: the check of the CPAT team's fix in 465, in red
        r = h.add_run(f' - {MARK[c465["status"]]}')
        r.font.color.rgb = RED
    lst, lnote = legacy_status(code)
    rows = [('Type', TYPE_NAME.get(typ, typ)), ('Priority', pri),
            ('Status in legacy', lst + (f': {lnote}' if lnote else '') + '.'), ('Legacy cells', where),
            ('What legacy does', what)]
    if fix:
        rows.append(('Fix legacy needs', fix))
    if effect:
        rows.append(('Effect', effect))
    rows.append(('In the prototype', status))
    rec = {r['id']: r for r in G.records()}.get(code)
    if rec and rec['former']:
        rows.insert(0, ('Former code', rec['former']))
    if rec and rec['see_also']:
        rows.append(('See also', rec['see_also']))
    if plan and plan.get('effect') and not effect:
        rows.append(('Effect (plan)', plan['effect']))
    if plan and plan.get('note'):
        rows.append(('Note (plan)', plan['note']))
    if plan:
        rows.append(('Cell plan', f'{len(plan.get("fixes", []))} cell(s), below' if plan.get('fixes')
                     else 'no cell to change (see the note)'))
    else:
        rows.append(('Cell plan', 'not written yet (Documentation: the bug-fixing procedure)'))
    t = doc.add_table(rows=0, cols=2)
    t.style = 'Table Grid'
    t.autofit = False
    for k, v in rows:
        c = t.add_row().cells
        shade(c[0], LIGHT)
        text(c[0], k, bold=True)
        p_ = text(c[1], v)
        if k == 'Status in legacy' and c465:
            p_.runs[0].font.color.rgb = RED
    fit_widths(t, [3.0, 14.0])
    doc.add_paragraph()
    if plan and plan.get('fixes'):
        table(doc, ['Cell', 'Formula now', 'New formula', 'Fill', 'Policy block'],
              [(f['cell'], f.get('now', ''), f.get('new', ''), f.get('fill', ''), f.get('policy', ''))
               for f in plan['fixes']], [1.6, 4.6, 4.6, 2.2, 3.0], size=7, mono_cols=(1, 2))


def bugs_part(doc):
    doc.add_heading('4. The legacy bugs in detail, by type', 1)
    allb = legacy_bugs()
    pl = plans()
    groups = [('power', '4.1 Engineer power model'), ('transport', '4.2 Engineer road-transport model'),
              ('other', '4.3 Other mitigation (prices, policies, ETS, emissions, revenue, GDP, results)')]
    n_by = {g: [b for b in allb if b[1] == g] for g, _h in groups}
    chk = check465()
    nc = sum(1 for c in chk if moved(c) == 'C')
    nb_ = sum(1 for c in chk if moved(c) == 'B')
    n_in = len([b for b in allb if b[1] == 'inputs'])
    para(doc, f'{len(allb) - n_in} legacy bugs of the mitigation sheets ({len(n_by["power"])} engineer power, '
              f'{len(n_by["transport"])} engineer transport, {len(n_by["other"])} other), {len(dist_bugs())} of the '
              f'distribution sheet, {n_in} of the inputs (MTInputs). Every one is fixed in the prototype' + (
                  f', except {", ".join(sorted(R.BUGS_REPLICATED))} (copied labels, no value effect; queued to fix)'
                  if R.BUGS_REPLICATED else '; none is replicated') + '. Within each type, the order is by priority, '
              'then by code.')
    nn = sum(1 for c, x in chk.items() if c.startswith('L') and x['status'] == 'Not fixed')
    p_ = para(doc, f'Legacy 465: the CPAT team marked {nc + nb_} of these bugs fixed in {LEGACY_FILE}; each fix was '
                   f'checked cell by cell against its plan (2026-10-22): {nc} confirmed (Appendix B), {nb_ - nn} fixed '
                   f'with caveats and {nn} not fixed (Appendix A). This part holds the bugs still open in legacy. '
                   'Every bug says its status in legacy.')
    p_.runs[0].font.color.rgb = RED
    n_by = {g: [b for b in v if not moved(b[0])] for g, v in n_by.items()}
    order = {'High': 0, 'Medium': 1, 'Low': 2}
    for g, h in groups:
        doc.add_heading(h, 2)
        if g == 'other':                             # v0.7.1: one table and set of cell plans per model area
            other_part(doc, n_by[g], pl, order)
            continue
        rows = sorted(n_by[g], key=lambda b: (order.get(b[7], 3), int(b[0][1:])))
        table(doc, ['Code', 'Priority', 'Title', 'Cell plan'],
              [(b[0], b[7], b[2], 'yes' if b[0] in pl else 'not yet') for b in rows], [1.4, 1.8, 10.8, 2.0])
        if g == 'power':                             # v0.6.4: from the former BugsIssuesUpgrades register
            power_effects(doc)
        for b in rows:
            bug_block(doc, b, pl.get(b[0]))
    doc.add_heading('4.4 Distribution', 2)
    para(doc, 'Legacy sheet Distribution (household incidence by decile). Fixed in the prototype v0.4.4; the fixes '
              'change Egypt\'s legacy numbers only a little (the targeted transfer of deciles 1-4 by up to 0.13 points '
              'of consumption, the Gini change with recycling by 0.0006 points; the urban and rural compensation '
              'shares most, since each now sums to 100). Method: Distribution_Method (section 3).')
    dist = [b for b in dist_bugs() if not moved(b[0])]
    table(doc, ['Code', 'Title', 'Cell plan'], [(b[0], b[2], 'yes' if b[0] in pl else 'not yet') for b in dist],
          [1.4, 12.6, 2.0])
    for b in dist:
        bug_block(doc, b, pl.get(b[0]))
    doc.add_heading('4.5 Inputs (MTInputs, ScenarioDefinition)', 2)
    para(doc, 'Bugs of the legacy input sheet MTInputs (the prototype\'s ScenarioDefinition). The inconsistencies '
              'that are issues (I85-I88) are in the Documentation and the tracker.')
    inp = [b for b in allb if b[1] == 'inputs' and not moved(b[0])]
    table(doc, ['Code', 'Priority', 'Title'], [(b[0], b[7], b[2]) for b in inp], [1.4, 1.8, 12.8])
    for b in inp:
        bug_block(doc, b, pl.get(b[0]))


def other_part(doc, bugs, pl, order):
    """v0.7.1: other mitigation by model area, sections in rough priority order, High/Medium/Low within each (the
    order of the section file within a priority). N1, N2 (found by the plans, not in the register) sit in their area."""
    by = {b[0]: b for b in bugs if not moved(b[0])}
    secs = other_sections()
    listed = {c for _t, _i, ids in secs for c in ids}
    rest = [c for c in by if c not in listed]
    if rest:
        secs.append(('Not yet sectioned', 'Bugs not yet assigned to an area (add them to cfg_other_sections.json).',
                     sorted(rest, key=lambda c: int(c[1:]))))
    para(doc, f'{len(by)} bugs in {len(secs)} sections by model area, ordered roughly by priority (sections holding '
              'High bugs first); within a section High, Medium, Low. Each section has its own table, then the cell '
              'plans. L135 and L136 were found by the cell plans (were N1, N2): confirm with the CPAT team before '
              'applying.')
    table(doc, ['#', 'Section', 'High', 'Medium', 'Low', 'Bugs'],
          [(str(i), t, *[str(sum(1 for c in ids if c in by and by[c][7].startswith(p_))) for p_ in
                         ('High', 'Medium', 'Low')], ', '.join(c for c in ids if c in by))
           for i, (t, _d, ids) in enumerate(secs, 1)], [0.8, 5.0, 1.2, 1.4, 1.0, 6.6], size=8)
    for i, (t, d, ids) in enumerate(secs, 1):
        doc.add_heading(f'4.3.{i} {t}', 3)
        para(doc, d, size=9)
        rows = sorted((by[c] for c in ids if c in by), key=lambda b: order.get(b[7].split()[0], 3))
        table(doc, ['Code', 'Priority', 'Title', 'Cell plan'],
              [(b[0], b[7], b[2], 'yes' if b[0] in pl else 'not yet') for b in rows], [1.4, 1.8, 10.8, 2.0])
        for b in rows:
            bug_block(doc, b, pl.get(b[0]), 4)


def power_effects(doc):
    """v0.6.4: the effect of each legacy power-model fix on the legacy Egypt inputs (power_model_ref)."""
    years = list(range(2022, 2041))
    k30, k40 = years.index(2030), years.index(2040)

    def kpi(o):
        gen = lambda k: sum(o['gen'][i][k] for i in range(9)) * 8.76 / 1000
        return {'gen30': gen(k30), 'gen40': gen(k40), 'co2_40': sum(o['co2'][i][k40] for i in range(9)),
                'gas40': o['shr'][1][k40], 'vre40': o['vre'][k40],
                'usd': sum(o['usd'][i][k] for i in range(9) for k in range(len(years))) / 1000}
    run = lambda case, fx: kpi(PM.engine(PM.legacy_inputs(case), years, fix=fx, shock=True))
    base = {c: run(c, frozenset()) for c in ('base', 'ctax')}
    pct = lambda a, z: '0' if abs(a / z - 1) < 5e-5 else f'{(a / z - 1) * 100:+.1f}%'
    rows = []
    for name in list(PM.FIXES) + ['all']:
        fx = PM.ALL_FIXES if name == 'all' else frozenset([name])
        b, c = run('base', fx), run('ctax', fx)
        label = ('All fixes together' if name == 'all' else R.POWER_EXTRA.get(name) or
                 f'L{[k for k, *_x in R.BUGS].index(name) + 1} {R.SHORT.get(name, name)}')
        rows.append((label, pct(b['gen30'], base['base']['gen30']), pct(b['gen40'], base['base']['gen40']),
                     pct(b['co2_40'], base['base']['co2_40']), pct(c['gas40'], base['ctax']['gas40']),
                     pct(c['vre40'], base['ctax']['vre40']), pct(b['usd'], base['base']['usd'])))
    doc.add_heading('Effect of each power fix (legacy Egypt inputs)', 3)
    para(doc, 'Change against legacy. Generation and CO2 from the baseline; gas and variable-renewable (VRE) shares '
              'from the carbon-tax run; investment is the 2022-2040 total of the baseline. Legacy levels: generation '
              f'{base["base"]["gen30"]:,.0f} TWh (2030) and {base["base"]["gen40"]:,.0f} TWh (2040); power CO2 '
              f'{base["base"]["co2_40"]:.1f} MtCO2 (2040); carbon-tax run gas share {base["ctax"]["gas40"]:.1%} and '
              f'VRE share {base["ctax"]["vre40"]:.1%} (2040); investment USD {base["base"]["usd"]:,.0f} bn. The '
              'effects do not add up exactly: the fixes interact.', size=9)
    table(doc, ['Fix', 'Generation 2030', 'Generation 2040', 'Power CO2 2040', 'Gas share 2040 (carbon tax)',
                'VRE share 2040 (carbon tax)', 'Investment'], rows, [4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0], size=7.5)


def doc_order():
    """Every legacy bug in the order of section 3 (power, transport, other mitigation by area, distribution)."""
    order = {'High': 0, 'Medium': 1, 'Low': 2}
    allb = legacy_bugs()
    out = []
    for g in ('power', 'transport'):
        out += sorted((b for b in allb if b[1] == g), key=lambda b: (order.get(b[7], 3), int(b[0][1:])))
    by = {b[0]: b for b in allb if b[1] == 'other'}
    for _t, _d, ids in other_sections():
        out += sorted((by.pop(c) for c in ids if c in by), key=lambda b: order.get(b[7].split()[0], 3))
    out += sorted(by.values(), key=lambda b: int(b[0][1:]))
    return out + dist_bugs()          # inputs bugs are in 'other' order (type inputs) via by


def appendices_465(doc):
    """v0.8.2: the bugs the CPAT team fixed in legacy 465, moved out of section 3 whole: B with caveats, C confirmed."""
    pl = plans()
    bugs = doc_order()
    for key, title, intro in (
            ('B', 'Appendix A. Bugs fixed with caveats in legacy CPAT 1.0pre_465',
             f'Bugs the CPAT team marked fixed in {LEGACY_FILE} whose fix is incomplete, differs from the plan, or was '
             'not found in the file (checked 2026-10-22, cell by cell against the plans). The red status says what '
             'remains. The issues I18 and I29, also on the team\'s list, are in the Documentation (nothing to fix '
             'in legacy).'),
            ('C', 'Appendix B. Bugs confirmed fixed in legacy CPAT 1.0pre_465',
             f'Bugs fixed in {LEGACY_FILE} as their cell plan says (checked 2026-10-22: baseline cell, filled range '
             'and policy copy compared with the plan). The "formula now" of these plans is the 456 formula moved to '
             '465 rows; 465 holds the new formula.')):
        sel = [b for b in bugs if moved(b[0]) == key]
        doc.add_page_break()
        doc.add_heading(title, 1)
        p_ = para(doc, intro + f' {len(sel)} bugs.')
        p_.runs[0].font.color.rgb = RED
        table(doc, ['Code', 'Priority', 'Title', 'Status in legacy'],
              [(b[0], b[7], b[2], legacy_status(b[0])[0]) for b in sel], [1.4, 1.8, 8.8, 4.0], size=8)
        for b in sel:
            bug_block(doc, b, pl.get(b[0]), 2)


def rule_part(doc):
    """v0.8.4 (user 2026-10-28): the rule up front; bugs here, issues in the Documentation and the tracker."""
    doc.add_heading('1. The rule: bugs and issues', 1)
    para(doc, 'Never replicate a legacy bug; always replicate a legacy issue, and track it (repository rule, NORMS 0). '
              'A bug is something legacy CPAT computes that it plainly does not intend: a reference to the wrong row, '
              'a copied formula that points to another sector, a unit applied twice. The prototype fixes it and this '
              'document records it with the cells and the fix legacy needs. An issue is something legacy does on '
              'purpose that is open to question (a method, a default, a convention): the prototype does what legacy '
              'does, and the issue is tracked. A departure from legacy that is not a bug fix is an exception, kept only '
              'by user decision.', 'The rule.')
    para(doc, 'Problems of the input data are issues (area Data): the prototype does exactly what legacy does with '
              'the data, unless the user decided otherwise. Where legacy reads the data wrongly (a blank read as 0), '
              'the fix is a formula change: a legacy bug with its cell plan, and the data problem stays an issue with '
              'priority Very high. Where no cell plan is possible, the prototype aligns with legacy and the issue has '
              'priority Extremely high (section 3).', 'Data.')
    table(doc, ['Code', 'Kind', 'What the prototype does', 'Where it is kept'],
          [(f'{p_}1-{p_}{max(int(re.search(r"[0-9]+", r["id"]).group(0)) for r in G.by_kind(p_))}', d,
            w, G.KINDS[p_][2] + f'; tracker {TRACKER_NAME}_v{R.REGISTER_VERSION}.xlsx')
           for p_, d, w in G.DEFINITIONS], [1.8, 7.4, 3.6, 3.2], size=8)
    para(doc, f'This document is about the legacy bugs (L). The issues (I, data included), prototype bugs (M), '
              f'departures (LD) and upgrades (U) are in the appendices of the '
              f'Documentation (CPAT-AI-Mitigation_Documentation.docx) and, with the bugs, in the tracker '
              f'{TRACKER_NAME}_v{R.REGISTER_VERSION}.xlsx, the master list (tabs Bugs and Issues). Every entry gives its '
              f'code, its former code where it was renumbered in v0.8.4, and the codes it relates to.', size=9)
    para(doc, f'Every cell reference is a row of the latest file from the CPAT team, {LEGACY_FILE} (sheet Mitigation '
              'unless stated); the bugs found in CPAT 1.0pre_456_NoPropData.xlsb were moved to 465 rows by matching '
              'labels and codes (legacy/bugfixes/data/rowmap_456_465.json). The procedure to fix a bug in the legacy '
              'workbook and confirm it all works is an appendix of the Documentation.', 'Legacy version.', size=9)


def stock_part(doc):
    """v0.8.4: one table of every legacy bug: found, fixed in the prototype, status in legacy 465."""
    doc.add_heading('2. Stock of legacy bugs: found and fixed', 1)
    bugs = G.by_kind('L')
    n = len(bugs)
    st = {k: sum(1 for r in bugs if r['legacy465'] == k) for k in ('Fixed', 'Fixed with caveats',
                                                                  'Not fixed (marked fixed)', 'Open')}
    fixed_p = sum(1 for r in bugs if not r['prototype'].startswith(('Not built', 'Kept', 'Copied')))
    table(doc, ['Legacy bugs', 'Number'], [
        ('Found (legacy 456 and 465)', n),
        ('Fixed in the prototype (or the feature not built; none replicated)', f'{fixed_p} fixed, {n - fixed_p} not '
                                                                              'built'),
        ('Fixed in legacy 465, confirmed cell by cell (2026-10-22)', st['Fixed']),
        ('Fixed with caveats in legacy 465', st['Fixed with caveats']),
        ('Marked fixed by the CPAT team but not fixed in 465', st['Not fixed (marked fixed)']),
        ('Still open in legacy 465', st['Open']),
        ('Data problems (section 3: bug L170, issues of area Data)', len(G.data_items()))], [12.0, 4.0], size=9)
    para(doc, 'One row per bug, in code order. Found: the legacy version and date of the find. In the prototype: '
              'what the prototype does. Legacy 465: the status of the CPAT team\'s fix. Details in part 4 (bugs '
              'still open in legacy) or Appendices A and B (fixed in 465).', size=9)
    short = lambda s: ('Not built' if s.startswith('Not built') else 'Fixed' if s.startswith(('Fixed', 'Fixed in'))
                       else s.split(':')[0].split('(')[0].strip()[:28])
    table(doc, ['Code', 'Former', 'Area', 'Bug', 'Priority', 'Found', 'In the prototype', 'Legacy 465'],
          [(r['id'], r['former'], r['area'].replace('Mitigation: ', ''), r['title'], r['priority'],
            ' '.join(str(x) for x in G.found(r['id'])[:2] if x), short(r['prototype']), r['legacy465'])
           for r in bugs], [1.1, 1.1, 2.2, 5.6, 1.3, 1.9, 1.8, 2.0], size=7)


def databugs_part(doc):
    """v0.8.5 (user 2026-10-29): the data problems, most urgent first: the bug with a cell plan and the issues."""
    doc.add_heading('3. Data problems', 1)
    para(doc, 'Problems of the input data, most urgent first. Extremely high: no cell plan is possible; the prototype '
              'does exactly what legacy does. Very high: a legacy bug covers it (cell plan in part 4); the data still '
              'need fixing. The issues are in full in the Documentation (appendix B) and the tracker.')
    table(doc, ['Code', 'Former', 'Kind', 'Priority', 'Title', 'In the prototype', 'Plan / next step', 'See also'],
          [(r['id'], r['former'], r['kind'], r['priority'], r['title'], r['prototype'], r['fix'], r['see_also'])
           for r in G.data_items()], [1.1, 1.6, 1.4, 1.5, 3.4, 2.8, 4.0, 1.2], size=7)


def export_json():
    """The whole register as one JSON file for code (v0.8.4: every kind and module, from register.py)."""
    pl = G.plans()
    recs = []
    for r in G.records():
        d = dict(r)
        p_ = pl.get(r['id'])
        d['cell_plan'] = None if p_ is None else {k: p_.get(k) for k in ('status', 'note', 'ref', 'fixes')}
        recs.append(d)
    out = {'title': f'Legacy CPAT bugs and the CPAT-AI register v{R.REGISTER_VERSION} (workbook v{B.VERSION})',
           'generated_by': 'excel_ai/bugs_and_legacy/register/make_bugfix_book.py', 'legacy_workbook': LEGACY_FILE,
           'kinds': {p_: {'kind': k, 'plural': pl_, 'kept_in': w} for p_, (k, pl_, w) in G.KINDS.items()},
           'definitions': [dict(zip(('code', 'definition', 'prototype'), d)) for d in G.DEFINITIONS],
           'other_mitigation_areas': [{'area': t_, 'about': d, 'codes': ids} for t_, d, ids in other_sections()],
           'records': recs}
    path = os.path.join(ROOT, 'bugs_and_legacy', 'register', 'Legacy_CPAT_Register.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=str)
    print('wrote', path)


def main():
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = 'Arial'
    st.font.size = Pt(10)
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = s.bottom_margin = Cm(2.0)
    doc.add_heading(f'Legacy CPAT bugs v{R.REGISTER_VERSION}', 0)
    para(doc, f'Version {R.REGISTER_VERSION}, {datetime.date.today().isoformat()}, the version of '
              f'CPAT-AI-Mitigation-Prototype v{B.VERSION}. Generated from the CPAT-AI repository '
              f'({os.path.basename(__file__)}). Legacy workbook: {LEGACY_FILE}. Master list: tracker '
              f'{TRACKER_NAME}_v{R.REGISTER_VERSION}.xlsx.', size=9)
    doc.add_heading('Contents', 1)
    toc(doc)
    rule_part(doc)
    doc.add_page_break()
    stock_part(doc)
    doc.add_page_break()
    databugs_part(doc)
    doc.add_page_break()
    bugs_part(doc)
    appendices_465(doc)
    doc.save(OUT)
    B.REL.publish(OUT)                            # v0.8.4: older versions to releases/
    print('wrote', OUT)
    export_json()


if __name__ == '__main__':
    main()
