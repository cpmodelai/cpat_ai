"""Update the CPAT team's tracker legacy/workbooks/Tracking issues.xlsx from the register (user 2026-10-18: "I put
a bug tracker in legacy folder. You could edit that by adding extra rows and extra columns. Continue to use our
codes").

Our part (user 2026-10-23): a divider sheet AI-FOUND->>, then BUGS (legacy bugs L, D) and ISSUES-OTHER (issues I, DI,
prototype bugs M, LegacyDiff rows LD), both with the same columns and the status in legacy first (bugs: from the check
of the fixes in legacy 465, bugsfixed/legacy465_check.json); Closed rows struck through, the filter shows Open rows.
Every row is refreshed from CPAT-AI_BugsAndIssues_latest.xlsx (run make_replication_lists and make_bugs_issues_sheet
first); codes no longer in the register stay, marked "Retired" with where they went; new codes are appended. Then a
divider PRIOR->> and the CPAT team's own sheets.

The team's sheets (CPAT_issues, Mit+Disn_DeepDive, MT_issues, Slicer_issues) keep their content and get two extra
columns: our code(s) and a short note, from data/tracker_mapping.json (or the file given as the first argument;
JSON {sheet: {item number: {"codes": [...], "note": "..."}}, "new_codes": [...]}; keys "Dist n" for the second
table of Mit+Disn_DeepDive, "General n" for its numbered general concerns). The new codes the mapping proposed are
in the register (v5.1: L95-L97, D9).

    python update_tracker.py [mapping.json]
"""
import copy
import json
import os
import re
import sys

import openpyxl
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.filters import CustomFilter, CustomFilters, FilterColumn

import issues_register as R
import make_bugfix_book as BK

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = '7.0'
TRACKER = os.path.join(HERE, '..', 'legacy', 'workbooks', 'Tracking issues.xlsx')
SHEET_SRC = os.path.join(HERE, '..', 'CPAT-AI_BugsAndIssues_latest.xlsx')
HEAD = 3                                                   # header row of BUGSandISSUES
BASE = 11                                                  # columns A-K: as our register export
EXTRA = ['Type', 'Code group', 'Settled in (prototype version)', 'Cell-level fix plan', 'Status in legacy 459',
         'Related CPAT team items', 'Updated']
MAPPING = os.path.join(HERE, '..', '..', 'data', 'mvp_legacy_extracts', 'tracker_mapping.json')   # team items -> our codes (kept with the register)
CHECK465 = os.path.join(HERE, '..', 'bugsfixed', 'legacy465_check.json')   # fixes checked in legacy 465 (2026-10-22)
TEAM = ['CPAT_issues', 'Mit+Disn_DeepDive', 'MT_issues', 'Slicer_issues']
GROUP = {'L': 'Legacy bug (mitigation)', 'D': 'Legacy bug (distribution)', 'DI': 'Issue (distribution)',
         'I': 'Issue (mitigation)', 'M': 'Prototype bug', 'LD': 'LegacyDiff row'}


def group(code):
    return GROUP[re.match(r'[A-Z]+', code).group(0)]


def order(code):
    pre = {'L': 0, 'D': 1, 'M': 2, 'I': 3, 'DI': 4, 'LD': 5}
    return pre[re.match(r'[A-Z]+', code).group(0)], int(re.search(r'\d+', code).group(0))


def current_rows():
    """{code: 11 values} of the register sheet, plus the distribution and prototype bugs and distribution issues."""
    ws = openpyxl.load_workbook(SHEET_SRC)['BUGSandISSUES']
    rows = {r[0]: list(r[:BASE]) for r in ws.iter_rows(min_row=HEAD + 1, values_only=True) if r[0]}
    for c, t, w, what, st in R.DIST_BUGS:
        rows.setdefault(c, [c, 'Legacy bug (distribution)', 'Low', t, 'No', 'Fixed', what, '', st, w, 'Closed'])
    for c, t, d, st in R.DIST_ISSUES:
        rows.setdefault(c, [c, 'Issue (distribution)', '', t, 'Yes' if st.startswith('Replicated') else 'No', st,
                            d, '', '', 'Methods, chapter Distribution', 'Open' if st.startswith('Replicated') else
                            'Closed'])
    for c, t, when, what, fix in R.MVP_BUGS:
        rows.setdefault(c, [c, 'Prototype bug', '', t, 'n/a', 'Fixed', what, '', fix, f'prototype {when}', 'Closed'])
    return rows


def successor(code):
    """Where a code that left the register went (from the register's own text 'was issue I8' etc.)."""
    pat = re.compile(rf'was (?:issue )?{code}\b')
    for c, t, *rest in R.LEGACY:
        if any(pat.search(str(x)) for x in rest):
            return f'Retired: now {c} ({t})'
    for row in getattr(R, 'UPGRADES', []):
        if any(pat.search(str(x)) for x in row[1:]):
            return f'Retired: now {row[0]} ({row[1]})'
    m = re.search(rf'{code} (v\d+\.\d+)', ' '.join(str(v) for v in R.ISSUE_STATUS.values()))
    if m:
        return f'Retired: replicated {m.group(1)} (closed)'
    if code.startswith('LD'):
        k = int(code[2:])
        if k <= len(BK.B.LEGACY_DIFFS):
            typ = BK.B.LEGACY_DIFFS[k - 1][5]
            return ('Retired: now as legacy (LegacyDiff "Same", closed)' if typ == 'Same' else
                    f'Retired: LegacyDiff "{typ}": a legacy bug fixed (see its L code)')
    return 'Retired: closed'


def type_of(code, kind):
    if code.startswith('L') and not code.startswith('LD'):
        return BK.TYPE_NAME[BK.bug_type(code)]
    if code.startswith('D'):
        return 'Distribution'
    if code.startswith('M'):
        return 'Prototype'
    return 'Issue' if code.startswith('I') else 'LegacyDiff'


def settled(values):
    m = re.search(r'\bv(\d+\.\d+)\b', ' '.join(str(v or '') for v in values[5:]))
    return m.group(1) if m else ''


def related(code, mapping):
    out = []
    for sheet in TEAM:
        for num, m in (mapping.get(sheet) or {}).items():
            if code in m.get('codes', []):
                out.append(f'{sheet} {num}')
    return '; '.join(out)


def style_like(ws, src_row, dst_row, ncols):
    for j in range(1, ncols + 1):
        s, d = ws.cell(src_row, j), ws.cell(dst_row, j)
        if s.has_style:
            d.font, d.fill, d.border = copy.copy(s.font), copy.copy(s.fill), copy.copy(s.border)
            d.alignment, d.number_format = copy.copy(s.alignment), s.number_format


# Our part of the tracker (user 2026-10-23): divider AI-FOUND->>, sheets BUGS (legacy bugs L, D) and ISSUES-OTHER
# (issues I, DI, prototype bugs M, LegacyDiff rows LD) with the same columns, status in legacy first; divider PRIOR->>,
# then the CPAT team's own sheets. Rows whose status starts with "Closed" are struck through; the filter shows Open.
OURS = ['AI-FOUND->>', 'BUGS', 'ISSUES-OTHER', 'PRIOR->>']
COLS = [  # header, width, key (old BUGSandISSUES header the value comes from, or a computed field)
    ('Ref', 8, 'Ref'), ('Status in legacy', 22, '_status'), ('Legacy check note (465)', 48, '_note'),
    ('Priority / severity', 12, 'Priority / severity'), ('Title', 46, 'Title'), ('Code group', 20, 'Code group'),
    ('Type', 18, 'Type'), ('Where in legacy / documented', 38, 'Where in legacy / documented'),
    ('What legacy does', 60, 'What legacy does'), ('Fix / next step', 52, 'Fix / next step'),
    ('Effect', 44, 'Effect'), ('Cell-level fix plan', 12, 'Cell-level fix plan'),
    ('Status in legacy 459', 18, 'Status in legacy 459'),
    ('Replicated in the prototype?', 20, 'Replicated in the prototype?'),
    ('How in the prototype', 28, 'How in the prototype'), ('Status in the prototype', 14, 'Status'),
    ('Settled in (prototype version)', 14, 'Settled in (prototype version)'),
    ('Related CPAT team items', 26, 'Related CPAT team items'), ('Updated', 12, 'Updated'), ('Kind', 22, 'Kind')]
OLD = ['Ref', 'Kind', 'Priority / severity', 'Title', 'Replicated in the prototype?', 'How in the prototype',
       'What legacy does', 'Effect', 'Fix / next step', 'Where in legacy / documented', 'Status'] + EXTRA
HEAD_FILL, CLOSED_GREY = 'FFEBF1DE', 'FF808080'


def existing_rows(wb):
    """{code: {old header: value}} from the sheet(s) of the previous run (BUGSandISSUES, or BUGS + ISSUES-OTHER)."""
    rows = {}
    if 'BUGSandISSUES' in wb.sheetnames:
        ws = wb['BUGSandISSUES']
        heads = [c.value for c in ws[HEAD]]
        for r in ws.iter_rows(min_row=HEAD + 1, values_only=True):
            if r[0]:
                rows[r[0]] = dict(zip(heads, r))
        return rows
    back = {h: k for h, _, k in COLS}
    for name in ('BUGS', 'ISSUES-OTHER'):
        if name in wb.sheetnames:
            ws = wb[name]
            heads = [back.get(c.value, c.value) for c in ws[HEAD]]
            for r in ws.iter_rows(min_row=HEAD + 1, values_only=True):
                if r[0]:
                    rows[r[0]] = dict(zip(heads, r))
    return rows


def is_bug(code):
    return bool(re.match(r'(L|D)\d', code)) and not code.startswith(('LD', 'DI'))


def legacy_status(code, row, check):
    """Status as legacy CPAT stands (bugs) or as the register has it (issues and the rest): 'Open ...' or 'Closed ...'."""
    st = str(row.get('Status') or '')
    if st.startswith('Retired'):
        return 'Closed (' + st[0].lower() + st[1:] + ')', ''
    if is_bug(code):
        c = check.get(code)
        if c is None:
            return 'Open', ''
        return {'Confirmed fixed': 'Closed (fixed in 465)', 'Fixed with caveats': 'Open (fixed with caveats in 465)',
                'Not fixed': 'Open (marked fixed, not fixed in 465)'}[c['status']], c['note']
    if code in check:                                       # I18, I29: prototype issues on the team's list
        return 'Closed (prototype issue; nothing to fix in legacy)', check[code]['note']
    if code.startswith('M'):
        return 'Closed (prototype bug, fixed)', ''
    m = {'Resolved': 'Closed (resolved)', 'Dropped': 'Closed (dropped)', 'Closed': 'Closed',
         'Accepted': 'Open (accepted: as legacy)', 'Open': 'Open'}
    return m.get(st, 'Open' + (f' ({st})' if st else ' (LegacyDiff)')), ''


def collect(wb, mapping, plans):
    """Rows of our two sheets as {code: {old header or _status/_note: value}}, in register order."""
    check = json.load(open(CHECK465, encoding='utf-8'))['bugs'] if os.path.exists(CHECK465) else {}
    cur, old = current_rows(), existing_rows(wb)
    codes = list(old) + sorted((c for c in cur if c not in old), key=order)
    out = {}
    for code in codes:
        if code in cur:
            row = dict(zip(OLD[:BASE], cur[code]))
        else:                                               # left the register: kept, marked
            row = {k: old[code].get(k) for k in OLD[:BASE]}
            row['Status'] = successor(code)
        vals = [row.get(k) for k in OLD[:BASE]]
        legacy = re.match(r'(L|D|I|DI)\d', code) and not code.startswith('LD')
        row.update({'Type': type_of(code, row.get('Kind')), 'Code group': group(code),
                    'Settled in (prototype version)': settled(vals),
                    'Cell-level fix plan': 'Yes' if code in plans else '',
                    'Status in legacy 459': 'Not reconciled yet' if legacy and code in cur else 'n/a',
                    'Related CPAT team items': related(code, mapping), 'Updated': f'v{VERSION}'})
        row['_status'], row['_note'] = legacy_status(code, row, check)
        out[code] = row
    return out


def write_sheet(wb, name, rows, title):
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name)
    body, head = Font(name='Arial', size=10), Font(name='Arial', size=10, bold=True)
    ws['A1'], ws['A1'].font = title, Font(name='Arial', size=12, bold=True)
    ws['A2'] = ('Our part of the tracker, written by excel_ai/mitigation/update_tracker.py from the register '
                '(issues_register.py) and the check of the legacy fixes (excel_ai/bugsfixed/legacy465_check.json). '
                'Status in legacy: Closed rows are struck through; the filter on column B shows the Open rows '
                '(clear it to see all). Details, fix procedure and cell plans: excel_ai/CPAT-AI_BugsAndIssues_latest.docx.')
    ws['A2'].font = Font(name='Arial', size=9, italic=True)
    fill = PatternFill('solid', fgColor=HEAD_FILL)
    side = Side(style='thin', color='FFBFBFBF')
    border = Border(left=side, right=side, top=side, bottom=side)
    for j, (h, w, _) in enumerate(COLS, 1):
        c = ws.cell(HEAD, j, h)
        c.font, c.fill, c.border = head, fill, border
        c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.column_dimensions[get_column_letter(j)].width = w
    r = HEAD
    for code, row in rows.items():
        r += 1
        for j, (_, _, k) in enumerate(COLS, 1):
            c = ws.cell(r, j, row.get(k))
            c.font, c.border = body, border
            c.alignment = Alignment(wrap_text=True, vertical='top')
        if str(row['_status']).startswith('Closed'):
            ws.row_dimensions[r].hidden = True              # the saved filter shows Open rows only
    last = get_column_letter(len(COLS))
    ws.freeze_panes = 'C4'
    ws.auto_filter.ref = f'A{HEAD}:{last}{r}'
    ws.auto_filter.filterColumn.append(FilterColumn(colId=1, customFilters=CustomFilters(
        customFilter=[CustomFilter(operator='notEqual', val='Closed*')])))
    ws.conditional_formatting.add(f'A{HEAD + 1}:{last}{r}', FormulaRule(
        formula=[f'LEFT($B{HEAD + 1},6)="Closed"'],
        font=Font(strike=True, color=CLOSED_GREY)))
    return ws, r - HEAD


def divider(wb, name, text, color):
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name)
    ws['A1'], ws['A1'].font = text, Font(name='Arial', size=14, bold=True)
    ws.sheet_properties.tabColor = color
    ws.column_dimensions['A'].width = 90
    return ws


def update_register_sheets(wb, mapping, plans):
    rows = collect(wb, mapping, plans)
    bugs = {c: r for c, r in rows.items() if is_bug(c)}
    other = {c: r for c, r in rows.items() if not is_bug(c)}
    divider(wb, 'AI-FOUND->>', 'Found by CPAT-AI (our codes): BUGS = legacy bugs (L mitigation, D distribution); '
            'ISSUES-OTHER = issues (I, DI), prototype bugs (M), LegacyDiff rows (LD). Same columns in both.', 'FF4F81BD')
    _, nb = write_sheet(wb, 'BUGS', bugs, 'Legacy CPAT bugs found by CPAT-AI: status in legacy')
    _, no = write_sheet(wb, 'ISSUES-OTHER', other, 'Issues, prototype bugs and LegacyDiff rows found by CPAT-AI')
    divider(wb, 'PRIOR->>', "The CPAT team's own tracker sheets (earlier items), with our codes added "
            '(columns CPAT-AI code(s), CPAT-AI note).', 'FF7F7F7F')
    if 'BUGSandISSUES' in wb.sheetnames:
        del wb['BUGSandISSUES']
    first = [wb[n] for n in OURS]
    wb._sheets = first + [s for s in wb._sheets if s.title not in OURS]
    wb.active = 1
    for s in wb._sheets:
        s.sheet_view.tabSelected = s.title == 'BUGS'
    return nb, no


def update_team_sheets(wb, mapping):
    n = 0
    for sheet in TEAM:
        if sheet not in wb.sheetnames or sheet not in mapping:
            continue
        ws = wb[sheet]
        hr = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value)    # header: first filled row
        heads = [ws.cell(hr, j).value for j in range(1, ws.max_column + 1)]
        if 'CPAT-AI code(s)' in heads:                       # rerun: the columns of the previous update
            ca = heads.index('CPAT-AI code(s)') + 1
            width, cb = ca - 1, ca + 1
        else:
            width = max(j for j in range(1, ws.max_column + 1) if ws.cell(hr, j).value)
            ca, cb = width + 1, width + 2
        for j, h in ((ca, 'CPAT-AI code(s)'), (cb, 'CPAT-AI note')):
            ws.cell(hr, j, h)
            src = ws.cell(hr, width)
            ws.cell(hr, j).font, ws.cell(hr, j).fill = copy.copy(src.font), copy.copy(src.fill)
            ws.cell(hr, j).border, ws.cell(hr, j).alignment = copy.copy(src.border), copy.copy(src.alignment)
        ws.column_dimensions[openpyxl.utils.get_column_letter(ca)].width = 16
        ws.column_dimensions[openpyxl.utils.get_column_letter(cb)].width = 48
        m = {str(k).strip(): v for k, v in mapping[sheet].items()}
        head, part = str(ws.cell(hr, 1).value), ''
        for r in range(hr + 1, ws.max_row + 1):
            a_, b_ = ws.cell(r, 1).value, str(ws.cell(r, 2).value or '')
            if a_ is not None and str(a_) == head:          # a second table (Mit+Disn_DeepDive: distribution)
                part = 'Dist '
                continue
            if a_ is None and re.match(r'\d+\.', b_):           # numbered lines without a number in A (General)
                key = 'General ' + b_.split('.')[0]
            else:
                key = (part + str(a_).strip()) if a_ is not None else ''
            if key in m:
                ws.cell(r, ca).value = ', '.join(m[key].get('codes', [])) or '-'
                ws.cell(r, cb).value = m[key].get('note', '')
                for j in (ca, cb):
                    ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
                    ws.cell(r, j).font = copy.copy(ws.cell(r, width).font)
                n += 1
    return n


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else MAPPING
    mapping = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
    wb = openpyxl.load_workbook(TRACKER)
    nb, no = update_register_sheets(wb, mapping, BK.plans())
    n = update_team_sheets(wb, mapping)
    wb.save(TRACKER)
    print(f'updated {TRACKER}: BUGS {nb} rows, ISSUES-OTHER {no} rows; team items mapped {n}')


if __name__ == '__main__':
    main()
