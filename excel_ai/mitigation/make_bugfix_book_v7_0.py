"""documentation/CPAT-AI-Mitigation-MVP_BugsAndIssues_v6.4.docx: the one Word register of bugs, issues and upgrades
(legacy CPAT and the prototype), with the bug-fixing procedure. v6.4: it replaces the three overlapping Word registers
(this book, CPAT-AI-Mitigation-MVP_BugsIssuesUpgrades and BUGSandISSUES): it gained a summary, the effect of each
power fix, the potential upgrades and the improvements made, and is written to the root folder documentation/.

Main text: the procedure to fix a bug in the legacy workbook and confirm it all works (excel_ai/legacy/bugfix_procedure,
updated). Then every legacy bug by type (engineer power, engineer transport, other mitigation, distribution), with the
cell-level fix plan where one exists (excel_ai/legacy/bugfixes/data/fixes_*.json), the issues (mitigation, distribution,
open LegacyDiff departures) and an appendix: one reference table in code order.

Sources: issues_register_v7_0.py (bugs, issues, status), make_legacy_fixes_v7_0.py (priority and the fix legacy
needs), build_v7_0.py (LegacyDiff), excel_ai/legacy/bugfixes/data (cell plans).

    python make_bugfix_book_v7_0.py        (needs python-docx)
"""
import datetime
import json
import os
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import build_v7_2 as B
import issues_register_v7_0 as R
import make_legacy_fixes_v7_0 as M
import power_model_ref_v7_0 as PM

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # excel_ai/ (restructure 2026-10-22)
PLANS = os.path.join(ROOT, 'legacy', 'bugfixes', 'data')   # v7.1: was excel_ai/legacy/bugfixes/
OUT = os.path.join(ROOT, f'{B.NAME}_BugsAndIssues_v{R.REGISTER_VERSION}.docx')   # v7.1.5: own version   # v6.4: root documentation/
HEAD, LIGHT, PALE = 'D9E8C4', 'F2F2F2', 'EBF1DE'
POWER = ({f'L{k}' for k in range(1, 13)} | {f'L{k}' for k in range(52, 57)}
         | {'L67', 'L83', 'L84', 'L88', 'L95'}
         | {f'L{k}' for k in range(107, 112)} | {'L126', 'L127'})   # v5.4: power features; v7.1: L126, L127   # engineer power model (L83, L84: electricity subsidies; L88: power)
TRANSPORT = {f'L{k}' for k in range(25, 42)}                                          # engineer road model
TYPE_NAME = {'power': 'Engineer power', 'transport': 'Engineer transport', 'other': 'Other mitigation',
             'dist': 'Distribution'}


# ---------------------------------------------------------------- the data
def bug_type(code):
    return 'power' if code in POWER else 'transport' if code in TRANSPORT else 'other'


def plans():
    """Cell-level plans by bug id (excel_ai/legacy/bugfixes/data; v7.1: every plan file, distribution included)."""
    out = {}
    for name in ('power_engineer', 'transport_engineer', 'other_mitigation', 'other_mitigation_2', 'distribution'):
        p = os.path.join(PLANS, f'fixes_{name}.json')
        if os.path.exists(p):
            for b in json.load(open(p, encoding='utf-8')):
                out[b['id']] = b
    return out


def other_sections():
    """v7.1: other-mitigation bugs by model area (excel_ai/legacy/bugfixes/data/cfg_other_sections.json), sections in
    rough priority order; a bug the file does not list goes to a last section."""
    cfg = json.load(open(os.path.join(PLANS, 'cfg_other_sections.json'), encoding='utf-8'))
    return [(s['title'], s['intro'], s['ids']) for s in cfg['sections']]


def legacy_bugs():
    """Every legacy bug: (code, type, title, where, what legacy does, fix, prototype status, priority, effect)."""
    rows = []
    for i, (_k, title, where, what, fix, why) in enumerate(R.BUGS):         # L1-L10 (engineer power)
        code = f'L{i + 1}'
        rows.append((code, 'power', title, f'Mitigation {where}', what, fix,
                     'Fixed in the prototype (v1.06-v1.08; power_model_ref with all fixes).',
                     M.PRIORITY.get(code, 'Low'), why))
    for code, title, where, what, status in R.LEGACY:                      # L11 onwards
        fix, effect = M.FIX.get(code, ('', ''))
        rows.append((code, bug_type(code), title, where, what, fix, status, M.PRIORITY.get(code, 'Low'), effect))
    rows.sort(key=lambda x: int(x[0][1:]))
    return rows


def dist_bugs():
    return [(c, 'dist', t, w, what, '', st, 'Low', '') for c, t, w, what, st in R.DIST_BUGS]


def plan_only():
    """Bugs found by the cell plans and not in the register (N1, N2): to confirm."""
    return [(b['id'], 'other', b['title'], b.get('where', ''), b.get('why', ''), '', 'Not in the register: confirm '
             'before applying.', b.get('pri') or 'Low', b.get('effect') or '') for k, b in plans().items()
            if k.startswith('N')]


def issues():
    st = R.ISSUE_STATUS
    out = []
    for code, title, desc, where in R.ISSUES:
        sev, status, nxt = st.get(code, ('', '', ''))
        out.append((code, title, desc, R.ISSUE_LEGACY.get(code, ''), sev, status, nxt, where))
    out.sort(key=lambda x: int(x[0][1:]))
    return out


def ld_open():
    """LegacyDiff rows whose type is not Same (departures still open or decided)."""
    out = []
    for k, (area, legacy, model, why, effect, typ) in enumerate(B.LEGACY_DIFFS, 1):
        if typ not in ('Same',):
            out.append((f'LD{k}', area, legacy, model, why, effect, typ))
    return out


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
BREAK = re.compile(r'([,;:(+\-*/=<>&!])')   # v5.4: break opportunities in long formulas (zero-width space after)


def fit_widths(t, widths):
    """v5.4 (user: tables overflowed on the right, left columns too wide): fixed layout, the grid and every cell
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
def procedure(doc):
    doc.add_heading('1. Purpose, scope and the rule for bugs and issues', 1)
    para(doc, 'This document collects every defect found in the legacy CPAT workbook while it was rebuilt as the '
              'CPAT-AI-Mitigation-MVP prototype, and the procedure to fix a defect in the legacy workbook and confirm '
              'that everything still works. The register is generated from the repository '
              f'(excel_ai/mitigation/issues_register_v{B.VERSION.replace(".", "_")}.py), so this document '
              f'and the prototype v{B.VERSION} say the same thing.')
    para(doc, 'A bug is something legacy CPAT computes that it plainly does not intend: a reference to the wrong row, '
              'a copied formula that points to another sector, a unit applied twice. An issue is something legacy '
              'does on purpose that is questionable (a method, a default, a data convention).', 'Bugs and issues.')
    para(doc, 'Bugs are never replicated in the prototype: each is fixed and recorded here with the legacy cells and '
              'the fix legacy needs. Issues are replicated (the prototype does what legacy does) and tracked, unless '
              'the user decided otherwise; the decision is recorded with the issue (repository rule NORMS 0, '
              '2026-10-15).', 'The rule.')
    para(doc, 'Every bug was read from CPAT 1.0pre_456_NoPropData.xlsb (sheet Mitigation unless stated). A newer '
              'file, CPAT 1.0pre_459_NoPropData.xlsb, arrived on 2026-10-18 with some bugs fixed by the CPAT team (one '
              'transport bug is not); the register has not yet been reconciled with it. Before applying a fix, run '
              'the preflight (section 2.3): it tells whether the cell still holds the bug.', 'Legacy version.')
    table(doc, ['Code', 'Meaning'], [
        ('L1-L80', 'Legacy bugs of the mitigation sheets (L17 was a prototype bug, L74 not used)'),
        ('D1-D8', 'Legacy bugs of the distribution sheet'),
        ('N1, N2', 'Defects found while writing the cell plans, not yet confirmed in the register'),
        ('M1-M12', 'Bugs of the prototype itself (fixed), kept for the record'),
        ('I1-I47', 'Issues of the mitigation module (replicated, not replicated by decision, or of the prototype)'),
        ('DI1-DI10', 'Issues of the distribution module'),
        ('LD1-LD66', 'Rows of the LegacyDiff sheet of the prototype: where it departs from legacy, and why')],
        [2.5, 13.5])


def procedure_steps(doc):
    doc.add_heading('2. The bug-fixing procedure', 1)
    doc.add_heading('2.1 The two protocols of the legacy workbook', 2)
    para(doc, 'Legacy CPAT relies on two conventions that a fix must keep, and that many bugs break:')
    table(doc, ['Protocol', 'What it means', 'Test'], [
        ('Drag left to right', 'Every year cell of a row holds the same formula in relative (R1C1) form, so a '
         'row can be dragged from its first year to the last.', 'One R1C1 formula per row from the first '
         'projected year to the last.'),
        ('Copy-paste baseline to policy', 'The policy block repeats the baseline block a fixed number of rows '
         'down: +6,331 rows from row 2173 (names BaselineFirstRow, PolicyScenarioFirstRow) to about row 6070, and '
         '+6,317 for the results sub-blocks after it (rows 6282-8404 map to 12599-14721).', 'The policy row equals '
         'the baseline row in R1C1 form.')], [3.5, 8.0, 4.5])
    doc.add_heading('2.2 Before you start', 2)
    bullets(doc, [
        'Work on a copy of the workbook; never fix the only copy, and save each fixed file as a new version.',
        'Find the cells by label and code (column D labels, column B/C codes), never by a typed row number: rows move '
        'between legacy versions.',
        'Check the register entry still matches the file: the cell must hold the formula the register describes. If '
        'it does not, stop and report (the bug may already be fixed, as in the 459 file).',
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
    para(doc, 'For almost every bug (the "Cell plan" column says which) the repository holds a cell-level plan '
              '(excel_ai/legacy/bugfixes/data, JSON): for each cell the formula now, the new formula, the range to fill and the policy row. Apply a '
              'plan as stage F above: type the new formula in the cell, fill the range, copy the baseline cells onto '
              'the policy row given (Paste Special, Formulas), recalculate, then run T1-T7. The plans are printed with '
              'each bug in section 3.')
    para(doc, 'For bugs without a cell plan yet the bug entry gives the legacy rows, what legacy does '
              'and the fix it needs. Write the plan as the existing ones were made (excel_ai/legacy/bugfixes/tools: build '
              'the new formula by exact text substitution of the legacy formula, stop if the legacy text is not found, '
              'check the brackets), add it to the JSON and regenerate this document.')
    doc.add_heading('2.5 Worked example: bug L1', 2)
    para(doc, 'L1 (services electricity demand grows with the industrial multiple after 2023) breaks both protocols, '
              'so one fix exercises every test: row 3731 holds =RC[-1]*R[-18]C in 2023 and =RC[-1]*R[-24]C from 2024 '
              '(the row cannot be dragged), and policy row 10062 has the same wrong formula.')
    table(doc, ['Check', 'Result (scratch copy of the NoPropData file, Excel 365, 2026-10-15)'], [
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
    doc.add_heading(f'{code}  {title}', level)
    rows = [('Type', TYPE_NAME.get(typ, typ)), ('Priority', pri), ('Legacy cells', where),
            ('What legacy does', what)]
    if fix:
        rows.append(('Fix legacy needs', fix))
    if effect:
        rows.append(('Effect', effect))
    rows.append(('In the prototype', status))
    if plan and plan.get('effect') and not effect:
        rows.append(('Effect (plan)', plan['effect']))
    if plan and plan.get('note'):
        rows.append(('Note (plan)', plan['note']))
    if plan:
        rows.append(('Cell plan', f'{len(plan.get("fixes", []))} cell(s), below' if plan.get('fixes')
                     else 'no cell to change (see the note)'))
    else:
        rows.append(('Cell plan', 'not written yet (section 2.4)'))
    t = doc.add_table(rows=0, cols=2)
    t.style = 'Table Grid'
    t.autofit = False
    for k, v in rows:
        c = t.add_row().cells
        shade(c[0], LIGHT)
        text(c[0], k, bold=True)
        text(c[1], v)
    fit_widths(t, [3.0, 14.0])
    doc.add_paragraph()
    if plan and plan.get('fixes'):
        table(doc, ['Cell', 'Formula now', 'New formula', 'Fill', 'Policy block'],
              [(f['cell'], f.get('now', ''), f.get('new', ''), f.get('fill', ''), f.get('policy', ''))
               for f in plan['fixes']], [1.6, 4.6, 4.6, 2.2, 3.0], size=7, mono_cols=(1, 2))


def bugs_part(doc):
    doc.add_heading('3. Legacy bugs by type', 1)
    allb = legacy_bugs()
    pl = plans()
    groups = [('power', '3.1 Engineer power model'), ('transport', '3.2 Engineer road-transport model'),
              ('other', '3.3 Other mitigation (prices, policies, ETS, emissions, revenue, GDP, results)')]
    n_by = {g: [b for b in allb if b[1] == g] for g, _h in groups}
    para(doc, f'{len(allb)} legacy bugs of the mitigation sheets ({len(n_by["power"])} engineer power, '
              f'{len(n_by["transport"])} engineer transport, {len(n_by["other"])} other), {len(R.DIST_BUGS)} of the '
              f'distribution sheet. Every one is fixed in the prototype; none is replicated. Within each type, the '
              f'order is by priority, then by code.')
    order = {'High': 0, 'Medium': 1, 'Low': 2}
    for g, h in groups:
        doc.add_heading(h, 2)
        if g == 'other':                             # v7.1: one table and set of cell plans per model area
            other_part(doc, n_by[g], pl, order)
            continue
        rows = sorted(n_by[g], key=lambda b: (order.get(b[7], 3), int(b[0][1:])))
        table(doc, ['Code', 'Priority', 'Title', 'Cell plan'],
              [(b[0], b[7], b[2], 'yes' if b[0] in pl else 'not yet') for b in rows], [1.4, 1.8, 10.8, 2.0])
        if g == 'power':                             # v6.4: from the former BugsIssuesUpgrades register
            power_effects(doc)
        for b in rows:
            bug_block(doc, b, pl.get(b[0]))
    doc.add_heading('3.4 Distribution', 2)
    para(doc, 'Legacy sheet Distribution (household incidence by decile). Fixed in the prototype v4.4; the fixes '
              'change Egypt\'s legacy numbers only a little (the targeted transfer of deciles 1-4 by up to 0.13 points '
              'of consumption, the Gini change with recycling by 0.0006 points; the urban and rural compensation '
              'shares most, since each now sums to 100). Method: Distribution_Method (section 3).')
    table(doc, ['Code', 'Title', 'Cell plan'], [(b[0], b[2], 'yes' if b[0] in pl else 'not yet') for b in dist_bugs()],
          [1.4, 12.6, 2.0])
    for b in dist_bugs():
        bug_block(doc, b, pl.get(b[0]))
    doc.add_heading('3.5 Bugs of the prototype (fixed, for the record)', 2)
    table(doc, ['Code', 'Title', 'Found / fixed', 'What happened', 'Fix'],
          [tuple(x) for x in R.MVP_BUGS], [1.2, 3.6, 2.2, 5.0, 4.0], size=7.5)


def other_part(doc, bugs, pl, order):
    """v7.1: other mitigation by model area, sections in rough priority order, High/Medium/Low within each (the
    order of the section file within a priority). N1, N2 (found by the plans, not in the register) sit in their area."""
    by = {b[0]: b for b in bugs + plan_only()}
    secs = other_sections()
    listed = {c for _t, _i, ids in secs for c in ids}
    rest = [c for c in by if c not in listed]
    if rest:
        secs.append(('Not yet sectioned', 'Bugs not yet assigned to an area (add them to cfg_other_sections.json).',
                     sorted(rest, key=lambda c: int(c[1:]))))
    para(doc, f'{len(by)} bugs in {len(secs)} sections by model area, ordered roughly by priority (sections holding '
              'High bugs first); within a section High, Medium, Low. Each section has its own table, then the cell '
              'plans. N1 and N2 were found by the cell plans and are not in the register: confirm before applying.')
    table(doc, ['#', 'Section', 'High', 'Medium', 'Low', 'Bugs'],
          [(str(i), t, *[str(sum(1 for c in ids if c in by and by[c][7].startswith(p_))) for p_ in
                         ('High', 'Medium', 'Low')], ', '.join(c for c in ids if c in by))
           for i, (t, _d, ids) in enumerate(secs, 1)], [0.8, 5.0, 1.2, 1.4, 1.0, 6.6], size=8)
    for i, (t, d, ids) in enumerate(secs, 1):
        doc.add_heading(f'3.3.{i} {t}', 3)
        para(doc, d, size=9)
        rows = sorted((by[c] for c in ids if c in by), key=lambda b: order.get(b[7].split()[0], 3))
        table(doc, ['Code', 'Priority', 'Title', 'Cell plan'],
              [(b[0], b[7], b[2], 'yes' if b[0] in pl else 'not yet') for b in rows], [1.4, 1.8, 10.8, 2.0])
        for b in rows:
            bug_block(doc, b, pl.get(b[0]), 4)


def issues_part(doc):
    doc.add_heading('4. Issues', 1)
    para(doc, 'Issues are intended behaviours of legacy (or of the prototype) that are questionable. Legacy side: '
              'replicated = the prototype does what legacy does; not replicated = a departure by user decision or '
              'still queued; mvp = an issue of the prototype with no legacy counterpart.')
    doc.add_heading('4.1 Mitigation module', 2)
    rows = issues()
    table(doc, ['Code', 'Title', 'Legacy side', 'Severity / status', 'Next step'],
          [(c, t, lg, f'{sev} / {st}', nxt) for c, t, _d, lg, sev, st, nxt, _w in rows], [1.2, 5.2, 2.2, 2.4, 5.0],
          size=7.5)
    for c, t, d, lg, sev, st, nxt, w in rows:
        doc.add_heading(f'{c}  {t}', 3)
        para(doc, d, size=9)
        para(doc, f'{lg}; {sev}, {st}. {nxt} Documented in: {w}.', 'Status:', size=9)
    doc.add_heading('4.2 Distribution module', 2)
    table(doc, ['Code', 'Title', 'Description', 'Status'], [tuple(x) for x in R.DIST_ISSUES], [1.4, 4.6, 7.4, 2.6],
          size=8)
    doc.add_heading('4.3 Departures from legacy still listed on the LegacyDiff sheet', 2)
    para(doc, 'Every row of the prototype\'s LegacyDiff sheet whose type is not "Same": a decision, a simplification, '
              'a part not built yet, or data.')
    table(doc, ['Row', 'Area', 'Prototype', 'Why', 'Type'],
          [(c, a, m, w, ty) for c, a, _l, m, w, _e, ty in ld_open()], [1.2, 3.0, 6.0, 4.2, 1.6], size=7)


def summary(doc):
    """v6.4: what the register holds, by part (from the former BugsIssuesUpgrades register)."""
    doc.add_heading('Summary', 1)
    n = {c: sum(1 for *_x, k in R.items() if k == c) for c in
         ('Legacy bug', 'MVP bug (fixed)', 'Known issue', 'Simplification / not yet', 'Upgrade')}
    up = {p_: sum(1 for u in R.UPGRADES if u[3] == p_) for p_ in ('High', 'Medium', 'Low')}
    para(doc, 'One register of everything that is wrong, questionable, simplified or still to do, in legacy CPAT and '
              'in the prototype. Every item has a code that the other documents use. The register is kept in '
              'issues_register_v7_0.py and the workbook sheet LegacyDiff; the full check tests that both agree.')
    table(doc, ['Part', 'Codes', 'Items', 'What it lists'],
          [('3. Legacy bugs by type', 'L, D', f'{n["Legacy bug"]}, {len(R.DIST_BUGS)}',
            'Defects of the legacy workbook (mitigation, distribution), with cell-level fix plans; all fixed in the '
            'prototype'),
           ('3.5 Bugs of the prototype', 'M', str(n['MVP bug (fixed)']), 'Defects of earlier prototype versions, all '
            'fixed'),
           ('4. Issues', 'I, DI', f'{n["Known issue"]}, {len(R.DIST_ISSUES)}', 'Questionable intended behaviours: '
            'replicated from legacy, departures, or issues of the prototype (status Open, Accepted, Resolved, Dropped)'),
           ('4.3 LegacyDiff departures', 'LD', str(len(ld_open())), 'Every difference with legacy that is not "Same" '
            f'({n["Simplification / not yet"]} of them simplifications, not yet built or to check)'),
           ('5. Potential upgrades', 'U', str(n['Upgrade']), f'{up["High"]} high, {up["Medium"]} medium, {up["Low"]} '
            'low priority')], [3.6, 1.4, 1.6, 9.4], size=8)
    bullets(doc, ['Rule (user 2026-10-15): legacy bugs are fixed, legacy issues are replicated and tracked.',
                  'Priorities: the Excel 365 review by the user (I1), the ETS goal seek tested by the user (I30), the '
                  'data requests (I64, I65, I13, I68). I62 and I71 are legacy issues, high priority for the CPAT team '
                  'but not for the prototype.'], size=9)


def power_effects(doc):
    """v6.4: the effect of each legacy power-model fix on the legacy Egypt inputs (power_model_ref)."""
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


def upgrades_part(doc):
    """v6.4: potential upgrades by priority and the improvements already made (former BugsIssuesUpgrades)."""
    doc.add_heading('5. Potential upgrades and improvements made', 1)
    for p_ in ('High', 'Medium', 'Low'):
        doc.add_heading(f'5.{("High", "Medium", "Low").index(p_) + 1} {p_} priority', 2)
        table(doc, ['Code', 'Upgrade', 'What and why'], [(i, t, d) for i, t, d, pr in R.UPGRADES if pr == p_],
              [1.2, 4.6, 10.2], size=8)
    doc.add_heading('5.4 Improvements already made in the prototype', 2)
    bullets(doc, [s.replace('**', '') for s in R.IMPROVEMENTS], size=9)
    doc.add_heading('5.5 Sources and how this register is kept consistent', 2)
    bullets(doc, ['issues_register_v7_0.py: the register (L, M, I, U items); LegacyDiff rows come from build_v7_0.py; '
                  'cell-level plans from excel_ai/legacy/bugfixes/data (fixes_*.json; the other-mitigation areas in '
                  'cfg_other_sections.json).',
                  f'{os.path.basename(OUT)[:-5]}.json: this whole register, cell plans included, as one JSON file for '
                  'code (written with this document).',
                  'BUGSandISSUES_v7_0.xlsx (make_bugs_issues_sheet_v7_0.py): the same register as one table, and the '
                  'CPAT team tracker (update_tracker_v7_0.py), for machines and filters.',
                  'check_v7_0.py: codes unique, every LegacyDiff row of these types included, workbook texts free of '
                  'stale statements, file references valid.',
                  'make_bugfix_book_v7_0.py builds this document (the power-fix effects are computed when it runs).'],
            size=9)


def appendix(doc):
    doc.add_heading('Appendix A. Reference table in code order', 1)
    pl = plans()
    rows = []
    for b in legacy_bugs():
        rows.append((b[0], f'Bug: {TYPE_NAME[b[1]].lower()}', b[2], b[7], 'fixed in the prototype',
                     'yes' if b[0] in pl else ''))
    for b in dist_bugs():
        rows.append((b[0], 'Bug: distribution', b[2], '', 'fixed in the prototype', ''))
    for b in plan_only():
        rows.append((b[0], 'Bug: to confirm', b[2], b[7], 'not in the register', 'yes'))
    for x in R.MVP_BUGS:
        rows.append((x[0], 'Prototype bug', x[1], '', 'fixed', ''))
    for c, t, _d, lg, sev, st, _n, _w in issues():
        rows.append((c, 'Issue: mitigation', t, sev, f'{lg}; {st}', ''))
    for c, t, _d, st in R.DIST_ISSUES:
        rows.append((c, 'Issue: distribution', t, '', st, ''))
    for c, a, _l, _m, _w, _e, ty in ld_open():
        rows.append((c, 'LegacyDiff', a, '', ty, ''))
    for c, t_, _d, pr in R.UPGRADES:                 # v6.4
        rows.append((c, 'Upgrade', t_, pr, 'potential', ''))
    pre = {'L': 0, 'D': 1, 'N': 2, 'M': 3, 'I': 4, 'DI': 5, 'LD': 6, 'U': 7}
    key = lambda r: (pre[re.match(r'[A-Z]+', r[0]).group(0)], int(re.search(r'\d+', r[0]).group(0)))
    rows.sort(key=key)
    table(doc, ['Code', 'Type', 'Title', 'Priority / severity', 'Status', 'Cell plan'], rows,
          [1.3, 2.8, 7.3, 1.7, 3.2, 1.2], size=7.5)


def export_json():
    """v7.1: the whole register as one JSON file next to the Word register (same content, for code)."""
    pl = plans()
    area = {c: t for t, _d, ids in other_sections() for c in ids}
    keys = ('code', 'type', 'title', 'where', 'what_legacy_does', 'fix', 'in_prototype', 'priority', 'effect')

    def bug(b):
        d = dict(zip(keys, b))
        d['type'] = TYPE_NAME.get(b[1], b[1])
        if b[1] == 'other':
            d['area'] = area.get(b[0], '')
        p_ = pl.get(b[0])
        d['cell_plan'] = None if p_ is None else {k: p_.get(k) for k in ('status', 'note', 'ref', 'fixes')}
        return d
    out = {
        'title': f'{B.NAME}: bugs, issues and upgrades v{R.REGISTER_VERSION} (workbook v{B.VERSION}; with legacy cell-level fix plans)',
        'generated_by': f'excel_ai/mitigation/make_bugfix_book_v{B.VERSION.replace(".", "_")}.py',
        'word_version': os.path.basename(OUT),
        'codes': 'L legacy bug (mitigation), D legacy bug (distribution), N found by the cell plans (not in the '
                 'register), M prototype bug (fixed), I issue, DI distribution issue, LD LegacyDiff departure, U upgrade',
        'other_mitigation_areas': [{'area': t, 'about': d, 'codes': ids} for t, d, ids in other_sections()],
        'legacy_bugs': [bug(b) for b in legacy_bugs() + plan_only()],
        'distribution_bugs': [bug(b) for b in dist_bugs()],
        'prototype_bugs': [dict(zip(('code', 'title', 'found_fixed', 'what_happened', 'fix'), x)) for x in R.MVP_BUGS],
        'issues': [dict(zip(('code', 'title', 'description', 'legacy', 'severity', 'status', 'next', 'where'), x))
                   for x in issues()],
        'distribution_issues': [dict(zip(('code', 'title', 'description', 'status'), x)) for x in R.DIST_ISSUES],
        'legacy_diff': [dict(zip(('code', 'area', 'legacy', 'model', 'why', 'effect', 'type'), x)) for x in ld_open()],
        'upgrades': [dict(zip(('code', 'title', 'description', 'priority'), x)) for x in R.UPGRADES],
    }
    path = os.path.join(ROOT, 'legacy', os.path.basename(OUT)[:-5] + '.json')   # the register for code
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
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
    t = doc.add_heading('CPAT-AI-Mitigation-MVP: bugs, issues and upgrades, with the bug-fixing procedure for '
                        'legacy CPAT', 0)
    para(doc, f'Register version {R.REGISTER_VERSION}, {datetime.date.today().isoformat()}. Generated from the CPAT-AI '
              f'repository for CPAT-AI-Mitigation-MVP v{B.VERSION} ({os.path.basename(__file__)}). Legacy workbook: CPAT 1.0pre_456_NoPropData.xlsb.',
         size=9)
    doc.add_heading('Contents', 1)
    toc(doc)
    summary(doc)
    doc.add_page_break()
    procedure(doc)
    procedure_steps(doc)
    doc.add_page_break()
    bugs_part(doc)
    doc.add_page_break()
    issues_part(doc)
    doc.add_page_break()
    upgrades_part(doc)
    doc.add_page_break()
    appendix(doc)
    doc.save(OUT)
    print('wrote', OUT)
    export_json()


if __name__ == '__main__':
    main()
